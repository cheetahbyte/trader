from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from common.own_types import Company, User, CompanyCreateModel
from common.user import get_current_active_user
from common.companies import get_companies, create_company, get_user_companies

router = APIRouter()


@router.get("/", dependencies=[Depends(get_current_active_user)])
async def get_companies_api():
    return list(await get_companies())


@router.get("/user")
async def get_user_companies_api(current_user: Annotated[User, Depends(get_current_active_user)]):
    return list(await get_user_companies(current_user))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company_api(current_user: Annotated[User, Depends(get_current_active_user)],
                             company: CompanyCreateModel) -> Company:
    return await create_company(current_user.id, company)
