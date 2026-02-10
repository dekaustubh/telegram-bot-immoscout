import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SEARCH_URLS = [
    "https://www.immobilienscout24.de/Suche/de/berlin/charlottenburg/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/wilmersdorf/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/schoeneberg/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/friedenau/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/prenzlauer-berg/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/mitte/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0"
]

bot = Bot(token=BOT_TOKEN)

def check():
    headers = {"User-Agent": "Mozilla/5.0"}

    found = set()

    for url in SEARCH_URLS:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href=True)

        for link in links:
            href = link["href"]

            if "/expose/" in href and href not in found:
                found.add(href)

                full_link = "https://www.immobilienscout24.de" + href

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🏠 New Berlin flat found:\n{full_link}"
                )

if __name__ == "__main__":
    check()
