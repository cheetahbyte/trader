import requests, bs4, database, time

base_dom: str = "https://www.onvista.de/aktien/aktien-laender"
counter: int = 0

def precise_capitalize(country_link) -> str:
    base = country_link.split("/")[-1].replace("-", " ").strip().split(" ")
    if len(base) == 3:
        return base[0].capitalize() + " " + base[1] + " " + base[2].capitalize()
    elif len(base) == 2:
        return base[0].capitalize() + " " + base[1].capitalize()
    else:
        return base[0].capitalize()


def insert(company_name: str, wkn: str, country: str, industry: str):
    db = database.Database()
    print("here")
    with open("stocks.txt", "a+") as f:
        f.write(wkn + "\n")
    db.add_company(company_name, wkn, country, industry)


def scrape_country(country_link: str):
    global counter
    if not "deutschland" in country_link:
        return
    r = requests.get("https://www.onvista.de" + country_link).content.decode('utf-8')
    soup = bs4.BeautifulSoup(r, "html.parser")
    all_companies = soup.select("tbody tr")
    print("Doing", precise_capitalize(country_link), "with ~", len(all_companies), "")
    for company in all_companies:
        print("Adding Company #%s" % counter)
        name = company.select("td a")[0].text.strip()
        if "ADR" in name:
            continue
        wkn, industry = company.select("td")[1:3]
        country = precise_capitalize(country_link)
        insert(name, wkn.text, country, industry.text)
        counter += 1


def scrape_base():
    resp = requests.get(base_dom).content.decode("utf-8")
    soup = bs4.BeautifulSoup(
        resp, "html.parser"
    )
    links = [x.get("href") for x in soup.select("tbody tr td a.link")]
    for link in links:
        if not link.endswith("laender"):
            scrape_country(link)


if __name__ == "__main__":
    start = time.time()
    scrape_base()
    end = time.time()
    print(round((end - start), 2), " seconds")
