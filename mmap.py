import argparse
import random
import re
from bs4 import BeautifulSoup
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 OPR/115.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/131.0.6778.73 Mobile/15E148 Safari/604.1",

    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.81 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.81 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 14; Mobile; rv:133.0) Gecko/133.0 Firefox/133.0",
]

PATTERNS = {
    "Emails": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "Phones": (
        r"(?:\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    ),
    "INN": r"\bИНН[\s:]*(\d{10}|\d{12})\b",
    "OGRN": r"\bОГРН(?:ИП)?[\s:]*(\d{13}|\d{15})\b",
}

BASE_WORDS = [
    "contact",
    "contacts",
    "contact-us",
    "contactus",
    "kontakt",
    "kontakty",
    "kontakti",
    "svyaz",
    "svyazatsya",
    "feedback",
    "about",
    "about-us",
    "aboutus",
    "o-nas",
    "onas",
    "o-kompanii",
    "okompanii",
    "company",
    "kompaniya",
    "info",
    "information",
    "informatsiya",
    "requisites",
    "rekvizity",
    "rekviziti",
    "details",
    "legal",
    "yuridicheskaya-informatsiya",
    "privacy",
    "privacy-policy",
    "politika-konfidentsialnosti",
    "terms",
    "terms-of-service",
    "oferta",
    "dogovor-oferty",
    "support",
    "help",
    "pomoshch",
    "podderzhka",
    "address",
    "adres",
    "adresa",
    "location",
    "locations",
    "filialy",
    "ofisy",
    "office",
    "offices",
    "team",
    "komanda",
    "staff",
    "sotrudniki",
    "rukovodstvo",
    "management",
    "directors",
    "imprint",
    "impressum",
]

WORDLIST = [""] + BASE_WORDS + [f"{w}.html" for w in BASE_WORDS]


def parse_contacts(html, url):
    text = BeautifulSoup(html, "html.parser").get_text(separator=" ")
    found = []
    for name, pattern in PATTERNS.items():
        matches = {
            m.strip() for m in re.findall(pattern, text, flags=re.IGNORECASE)
        }
        if matches:
            found.append(f"  {name}: {', '.join(matches)}")
    if found:
        print(f"\n[\33[32m+\33[0m] {url}\n" + "\n".join(found))


def scan_site(base_url):
    base_url = base_url.rstrip("/")
    session = requests.Session()

    for path in WORDLIST:
        url = f"{base_url}/{path}" if path else base_url
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        try:
            res = session.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                parse_contacts(res.text, url)
        except requests.RequestException:
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="vanya_scanner.py")
    parser.add_argument("--url", required=True, help="Target URL")
    args = parser.parse_args()
    scan_site(args.url)
