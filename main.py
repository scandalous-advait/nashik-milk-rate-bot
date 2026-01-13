import os
import requests
import feedparser
import datetime

# Secrets (We will set these in Step 3)
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=Nashik+milk+rate+procurement+mandi&hl=en-IN&gl=IN&ceid=IN:en"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_rates():
    feed = feedparser.parse(RSS_URL)
    
    updates_found = False
    today = datetime.date.today().strftime("%d %b %Y")
    message = f"🥛 **Daily Milk Rate Check ({today})**\n\n"
    
    if feed.entries:
        for entry in feed.entries[:3]:
            # Filter for relevant keywords to reduce noise
            if any(word in entry.title.lower() for word in ['milk', 'rate', 'price', 'dudh', 'lakh']):
                message += f"• [{entry.title}]({entry.link})\n\n"
                updates_found = True
    
    # Only send if we found news OR if it's a Monday (weekly heartbeat check)
    if updates_found:
        send_telegram_message(message)
    elif datetime.datetime.today().weekday() == 0: # Optional: confirm bot is alive on Mondays
        send_telegram_message("No specific milk rate news today. Bot is active.")

if __name__ == "__main__":
    check_rates()
