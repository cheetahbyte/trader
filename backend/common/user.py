import typing, os
import uuid
from jose import jwt
from fastapi import Depends, HTTPException, status
from common.db import DB
from common.own_types import User, UserInDB, TokenData, UserCreateModel
from database import database
from datetime import timedelta, timezone, datetime
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import bcrypt

SECRET_KEY = os.getenv('SECRET_KEY') or "1"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_user(db: database.Database, username: str) -> UserInDB | None:
    conn = await db.gimme()
    try:
        user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
    finally:
        await db.pool.release(conn)
    return UserInDB(**user)


def verify_password(plain_password, hashed_password) -> bool:
    print(plain_password, hashed_password)
    return bcrypt.checkpw(plain_password.strip().encode("utf-8"), hashed_password.strip().encode("utf-8"))


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(db: database.Database, username: str, password: str) -> bool | UserInDB:
    user = await get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: typing.Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    user = await get_user(DB, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: typing.Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_user(user: UserCreateModel) -> User:
    print("create", user.password)
    conn = await DB.gimme()
    try:
        await conn.execute(
            "INSERT INTO users (id, username, email, hashed_password) VALUES($1, $2, $3, $4) returning id, username, email, full_name, disabled;",
            uuid.uuid4(), user.username, user.email,
            bcrypt.hashpw(user.password.strip().encode("utf-8"), bcrypt.gensalt()).decode("utf-8").strip())
        user = await conn.fetchrow("select id, username, email, full_name, disabled from users where username=$1;", user.username)
    finally:
        await DB.pool.release(conn)
    return user
