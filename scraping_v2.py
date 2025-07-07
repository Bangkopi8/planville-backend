
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime

BASE_URL = "https://planville.de"
PAGES = ["", "/leistungen", "/kontakt", "/foerderung", "/ueber-uns"]

def clean_text(text):
    return ' '.join(text.split())

def scrape_page(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(['p', 'h1', 'h2', 'li'])
        result = []
        for el in elements:
            txt = clean_text(el.get_text(strip=True))
            if len(txt) >= 30:
                result.append({
                    "text": txt,
                    "source": url,
                    "scraped_at": datetime.now().isoformat()
                })
        return result
    return []

def scrape_planville():
    all_data = []
    for page in PAGES:
        full_url = urljoin(BASE_URL, page)
        try:
            all_data.extend(scrape_page(full_url))
        except Exception as e:
            print(f"[ERROR] {full_url} – {e}")

    with open("data/docs_v2.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_planville()
