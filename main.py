import os
import requests
import feedparser
import datetime

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=Nashik+milk+rate+procurement+mandi&hl=en-IN&gl=IN&ceid=IN:en"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_rates():
    print("Checking news feed...")
    
    # 1. DEFINE THE DATE (This was missing causing your error)
    today_str = datetime.date.today().strftime("%d %b %Y")
    
    feed = feedparser.parse(RSS_URL)
    updates_found = False
    message = f"🥛 **Milk Rate News ({today_str})**\n\n"
    
    # 2. CHECK NEWS
    if feed.entries:
        for entry in feed.entries[:5]:
            title = entry.title.lower()
            if 'milk' in title and any(w in title for w in ['rate', 'price', 'hike', 'procurement', 'dudh']):
                message += f"• [{entry.title}]({entry.link})\n\n"
                updates_found = True
    
    # 3. SENDING LOGIC (For Demo: Always send a message)
    if updates_found:
        send_telegram_message(message)
        print("News found! Message sent.")
    else:
        # This will send a 'No News' update so your team sees the bot working
        send_telegram_message(f"📉 **Daily Update ({today_str}):** No significant milk rate changes found in the news today.")
        print("No news, but sent daily summary.")

if __name__ == "__main__":
    check_rates()
