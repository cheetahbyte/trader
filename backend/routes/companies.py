from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from common.own_types import Company, User
from common.user import get_current_active_user
from common.companies import get_companies

router = APIRouter()


@router.get("/")
async def get_companies(current_user: Annotated[User, Depends(get_current_active_user)]):
    return list(await get_companies(current_user))
