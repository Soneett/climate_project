import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://econom22.ru/prognoz/program/reg_programms/gos_programms/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def extract_period(text):
    m = re.search(r"(\d{4})\s*[–-]\s*(\d{4})", text)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def parse_main_list():
    soup = get_soup(BASE_URL + "index.php")

    year_from, year_to = extract_period(
        soup.get_text(" ", strip=True)
    )

    programs = {}

    rows = soup.select("table tr")[1:]

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 4:
            continue

        name = clean_text(tds[1].get_text(" ", strip=True))
        executor = clean_text(tds[2].get_text(" ", strip=True))

        link = None
        a = tds[3].find("a", href=True)
        if a:
            link = urljoin(BASE_URL, a["href"])

        if name not in programs:
            programs[name] = {
                "program_name": name,
                "registry_link": link,
                "period_from": year_from,
                "period_to": year_to,
                "source_page": BASE_URL + "index.php",
                "executors": [executor] if executor else []
            }
        else:
            if programs[name]["registry_link"] is None and link:
                programs[name]["registry_link"] = link

    return list(programs.values())


def main():
    programs = parse_main_list()
    print(f"Найдено программ: {len(programs)}")

    for p in programs:
        print(p)


if __name__ == "__main__":
    main()



