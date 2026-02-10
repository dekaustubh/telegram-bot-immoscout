import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# YOUR SETTINGS
BOT_TOKEN = "8419431191:AAG2K2xTZ17vA98-gRKlk1RAtcQ4cDWeTCE"
CHAT_ID = "8252624154"

SEARCH_URLS = [
    "https://www.immobilienscout24.de/Suche/de/berlin/charlottenburg/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/wilmersdorf/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/schoeneberg/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
    "https://www.immobilienscout24.de/Suche/de/berlin/friedenau/wohnung-mieten?numberofrooms=3.0-&livingspace=75.0-&price=-1900.0",
]

CHECK_INTERVAL = 30  # seconds

bot = Bot(token=BOT_TOKEN)
seen = set()

def check():
    global seen

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for url in SEARCH_URLS:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        listings = soup.select("article")

        for listing in listings:
            link = listing.find("a", href=True)
            if not link:
                continue

            full_link = "https://www.immobilienscout24.de" + link["href"]

            if full_link not in seen:
                seen.add(full_link)

                print("New:", full_link)

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🏠 New flat found:\n{full_link}"
                )

def main():
    print("Bot started...")
    bot.send_message(chat_id=CHAT_ID, text="Berlin Flat Bot started")

    while True:
        try:
            check()
        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

main()

