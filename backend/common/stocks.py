from common.own_types import Stock
from common.db import DB
from datetime import datetime


async def get_stock(wkn: str, fr: datetime = None, to: datetime = datetime.now(), steps: int = 5) -> list[Stock]:
    conn = await DB.gimme()
    stocks: list[Stock] = []
    try:
        c = await conn.fetch("SELECT * FROM aktien WHERE wkn=$1", wkn)
        for row in c:
            stock_data = dict(**row)
            stock_data.pop("site")
            stock_data["value"] = round(stock_data["value"], 2)
            stocks.append(Stock(**stock_data))
    finally:
        await DB.pool.release(conn)

    return stocks
