from common.db import DB
from common.own_types import Company, CompanyCreateModel, User
import uuid


async def get_companies() -> list[Company]:
    conn = await DB.gimme()
    companies = []
    try:
        c = await conn.fetch("SELECT * FROM companies;")
        for row in c:
            company = Company(**row)
            companies.append(company)
    finally:
        await DB.pool.release(conn)
    return companies


async def get_user_companies(user: User) -> list[Company]:
    default_companies = await get_companies()
    conn = await DB.gimme()
    user_companies = []
    try:
        c = await conn.fetch("SELECT * FROM companies where user=$1;", str(user.id))
        for row in c:
            user_companies.append(Company(**row))
    finally:
        await DB.pool.release(conn)
    return user_companies + default_companies


async def create_company(user_id: uuid.UUID, comp: CompanyCreateModel) -> Company | None:
    conn = await DB.gimme()
    company: Company | None = None
    try:
        await conn.fetchrow("INSERT INTO companies VALUES ($1, $2, $3, $4)", comp.wkn, comp.company,
                            comp.country, user_id)
        c = await conn.fetchrow("select * from companies where wkn = $1", comp.wkn)
        company = Company(**c)
    finally:
        await DB.pool.release(conn)
    return company
