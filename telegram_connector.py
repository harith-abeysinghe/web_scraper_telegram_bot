import os
import requests
from db_connection import connect_to_mongodb  # Importing the connection function
from datetime import datetime, timedelta
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Connect to MongoDB
collection = connect_to_mongodb()

def send_to_telegram(message: str, bot_token: str, channel_id: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    params = {
        'chat_id': channel_id,
        'text': message
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print("Message sent successfully!")
        return True
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        return False


def send_unsent_news():
    # Current time for comparison
    now = datetime.now()

    # Fetch unsent news from MongoDB
    unsent_news = collection.find({"sentToChannel": {"$ne": True}})

    # Process each news item
    for news in unsent_news:
        # Check if the news is within 24 hours
        try:
            news_timestamp = datetime.fromisoformat(news.get("timestamp", now.isoformat()))
        except ValueError:
            print(f"Invalid timestamp for news: {news.get('title')}. Using current time.")
            news_timestamp = now

        if now - news_timestamp < timedelta(hours=48):
            # Send the news to Telegram
            title = news.get("title", "No Title")
            source = news.get("source", "Unknown Source")
            message = f"{title}\n\nSource: {source}"
            time.sleep(5)
            sent = send_to_telegram(message, BOT_API_TOKEN, CHANNEL_ID)

            # If the news was sent, update the 'sentToChannel' field in MongoDB
            if sent:
                collection.update_one({"_id": news["_id"]}, {"$set": {"sentToChannel": True}})

    print("All unsent news has been processed and updated in MongoDB.")

send_unsent_news()
