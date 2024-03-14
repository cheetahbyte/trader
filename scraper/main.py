import database
import schedule
import scraper
import time
import ingest_stocks

def dummy(x):
    print("HI", x)


def do(wkn: str):
    try:
        database.Database().insert(scraper.get(wkn))
    except IndexError:
        print(wkn)


def main():
    companies: list[str] = [c[0] for c in database.Database().get_all_companies_wkn()]
    for company in companies:
        schedule.every(1).minutes.do(do, company)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    if len(database.Database().get_all_companies_wkn()) == 0:
        ingest_stocks.enter_stocks()
    main()
