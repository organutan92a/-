import os
from telethon import TelegramClient
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Telegram credentials
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
telegram_channel = os.getenv("TELEGRAM_CHANNEL")  # no @

# RSS feed from .env
RSS_FEED_URL = os.getenv("INSTAGRAM_RSS_FEED")
AFFILIATE_MESSAGE = os.getenv("AFFILIATE_MESSAGE", "")

client = TelegramClient("userbot_session", api_id, api_hash)

def get_latest_rss_post():
    try:
        response = requests.get(RSS_FEED_URL, timeout=10)
        if response.status_code == 200 and "<item>" in response.text:
            from xml.etree import ElementTree
            tree = ElementTree.fromstring(response.content)
            items = tree.findall(".//item")
            if items:
                latest = items[0]
                title = latest.find("title").text
                link = latest.find("link").text
                return f"{title}\n{link}{AFFILIATE_MESSAGE}"
    except Exception as e:
        print(f"Error fetching RSS: {e}")
    return None

async def test_send():
    post = get_latest_rss_post()
    if post:
        await client.send_message(telegram_channel, post)
        print(f"✅ Sent post: {post}")
    else:
        print("❌ No post found or failed to fetch.")

with client:
    client.loop.run_until_complete(test_send())
