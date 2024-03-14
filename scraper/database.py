import typing

import psycopg2
from config import load_config
from own_types import Stock


class Database:
    config = load_config()

    def insert(self, s: Stock):
        """Inserts a stock into the database"""
        try:
            with psycopg2.connect(**self.config) as conn:
                cur = conn.cursor()
                cur.execute("""INSERT INTO "aktien" VALUES(%s,%s,%s,%s)""", (s.wkn, s.value, s.date, s.site))
                conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def add_company(self, company_name: str, wkn: str, country: str):
        """Adds a company in the database"""
        try:
            with psycopg2.connect(**self.config) as conn:
                cur = conn.cursor()
                cur.execute("""INSERT INTO "companies" VALUES(%s,%s,%s)""", (wkn, company_name, country))
                conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def get_all_companies_wkn(self) -> list[typing.Any]:
        """Returns all companies in the database"""
        try:
            with psycopg2.connect(**self.config) as conn:
                cur = conn.cursor()
                cur.execute("""select wkn from companies;""")
                x = cur.fetchall()
                return list(x)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
