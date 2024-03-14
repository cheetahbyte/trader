import datetime
import random, requests
from own_types import Stock, Website
from lxml import etree
import bs4

sites: list[str] = [
    "https://www.tagesschau.de/wirtschaft/boersenkurse/suche/?suchbegriff=%s",
]


class Scrapings:
    @staticmethod
    def scrape_tagesschau(content: str) -> float:
        soup = bs4.BeautifulSoup(content, "html.parser")
        try:
            return float(str(soup.select("tr.linked td.ri span.icon_pos")[0].contents[0]).replace(",", "."))
        except IndexError:
            return float(str(soup.select("tr.linked td.ri span.icon_neg")[0].contents[0]).replace(",", "."))


def scrape(wkn: str) -> [float, Website]:
    """this function retrieves a stock object from the website and scrapes its value"""
    site = random.choice(sites) % wkn
    resp = requests.get(site, ).content.decode('utf-8')
    index: int = sites.index(site.rstrip(wkn) + "%s")
    match index:
        case Website.Tagesschau:
            return Scrapings.scrape_tagesschau(resp), Website.Tagesschau
        case _:
            return -1, Website.NotFound


def validate(n: int, s: Stock) -> True | False:
    """this function validates the stock object and returns True or False"""
    pass


def get(wkn: str) -> Stock:
    value, site = scrape(wkn)
    return Stock(wkn, value, datetime.datetime.now(), site)
