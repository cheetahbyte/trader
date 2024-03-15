from common.db import DB
from common.own_types import Company


async def get_companies() -> list[Company]:
    conn = await DB.gimme()
    companies = []
    try:
        companies = await conn.fetch("SELECT * FROM companies;")
        for row in companies:
            print(row)
            company = Company(**row)
            companies.append(company)
    finally:
        await DB.pool.release(conn)
    return companies
