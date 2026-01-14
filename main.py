import os
import requests
import datetime
import re

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SERP_API_KEY = os.environ.get("SERPAPI_KEY")

# The exact search query you asked for
SEARCH_QUERY = "current cow milk procurement rate nashik 2026"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_google_rate():
    # 1. CALL THE SERP API (Google Search as an API)
    url = "https://serpapi.com/search.json"
    params = {
        "q": SEARCH_QUERY,
        "api_key": SERP_API_KEY,
        "location": "Nashik, Maharashtra, India",
        "hl": "en",
        "gl": "in",
        "num": 3  # We only need top 3 results
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
    except Exception as e:
        return None, f"⚠️ Error connecting to Google: {e}"

    # 2. EXTRACT THE NUMBER
    # We look for the "answer_box" (Google's direct answer) or the top snippet
    found_text = ""
    source_link = ""
    
    # Priority 1: Google's "Direct Answer" box
    if "answer_box" in data and "snippet" in data["answer_box"]:
        found_text = data["answer_box"]["snippet"]
        source_link = data["answer_box"].get("link", "")
    
    # Priority 2: The top organic result snippet
    elif "organic_results" in data:
        first_result = data["organic_results"][0]
        found_text = first_result.get("snippet", "")
        source_link = first_result.get("link", "")

    # 3. FIND THE PRICE (Regex to find ₹xx or Rs xx)
    # Looks for patterns like "₹ 42" or "Rs. 42.50"
    price_match = re.search(r'(?:Rs\.?|₹)\s?(\d+(?:\.\d{1,2})?)', found_text, re.IGNORECASE)
    
    if price_match:
        price = price_match.group(1) # The number found (e.g., "42")
        return price, source_link
    else:
        return None, source_link

def run_bot():
    print("Searching Google for rates...")
    price, link = get_google_rate()
    today_str = datetime.date.today().strftime("%d %b %Y")
    
    if price:
        # SUCCESS: We found a number!
        msg = (
            f"🥛 **Daily Rate Check ({today_str})**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔍 **Found Rate:** ₹{price} / Litre\n"
            f"🔗 [Source Link]({link})\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
    else:
        # FALLBACK: We found a link but no clear number
        msg = (
            f"🥛 **Daily Rate Check ({today_str})**\n"
            f"I searched for '{SEARCH_QUERY}' but couldn't auto-read the exact number today.\n\n"
            f"👇 **Click here to check manually:**\n"
            f"[View Google Search Result]({link})"
        )

    send_telegram_message(msg)
    print("Update sent.")

if __name__ == "__main__":
    run_bot()
