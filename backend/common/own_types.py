import pydantic
import uuid


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str | None = None


class User(pydantic.BaseModel):
    id: uuid.UUID
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class UserCreateModel(pydantic.BaseModel):
    username: str
    email: str
    password: str


class Company(pydantic.BaseModel):
    wkn: str
    company: str
    country: str