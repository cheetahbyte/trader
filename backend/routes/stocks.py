from fastapi import Depends, HTTPException, status, APIRouter
from common.user import get_current_active_user
from common.stocks import get_stock
from common.own_types import Stock

router = APIRouter()


@router.get("/", dependencies=[Depends(get_current_active_user)])
async def return_stock(wkn: str) -> list[Stock]:
    return await get_stock(wkn)
