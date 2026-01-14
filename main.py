import os
import requests
import feedparser
import datetime

# Secrets
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=Nashik+milk+rate+procurement+mandi&hl=en-IN&gl=IN&ceid=IN:en"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    print(f"Attempting to send message to ID: {CHAT_ID}...")
    response = requests.post(url, json=payload)
    
    # PRINT THE RESULT FROM TELEGRAM
    print(f"Telegram Response Code: {response.status_code}")
    print(f"Telegram Response Text: {response.text}")

def check_rates():
    # 1. FORCE A MESSAGE FOR TESTING
    print("Starting test run...")
    send_telegram_message("🔔 **Test Message:** The bot is connected to this group successfully.")

    # 2. PROCEED WITH NORMAL CHECK
    feed = feedparser.parse(RSS_URL)
    updates_found = False
    message = "🥛 **News Found:**\n\n"
    
    if feed.entries:
        for entry in feed.entries[:3]:
            if any(word in entry.title.lower() for word in ['milk', 'rate', 'price', 'dudh', 'lakh']):
                message += f"• [{entry.title}]({entry.link})\n\n"
                updates_found = True
    
    # --- SENDING LOGIC ---
    if updates_found:
        send_telegram_message(message)
        print("News found! Message sent.")
    else:
        # For your demo/team: Always send a message even if no news
        send_telegram_message(f"📉 **Daily Update ({today_str}):** No significant milk rate changes found in the news today.")
        print("No news, but sent daily summary.")

if __name__ == "__main__":
    check_rates()
