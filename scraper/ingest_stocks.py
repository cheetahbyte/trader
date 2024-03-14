import csv
import database
import time


def insert(company_name: str, wkn: str, country: str) -> None:
    db = database.Database()
    db.add_company(company_name, wkn, country)


def enter_stocks():
    with open("stocks.txt", "r") as f:
        csv_reader = csv.reader(f, delimiter=';')
        lnct: int = 0
        for row in csv_reader:
            if not lnct == 0:
                print(row)
                insert(row[1].strip(), row[0].strip(), row[2].strip())
            lnct += 1


if __name__ == "__main__":
    enter_stocks()
