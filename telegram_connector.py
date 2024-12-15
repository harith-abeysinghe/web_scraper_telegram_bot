import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

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


def send_unsent_news(json_file: str = "news_data.json"):
    # Load the news data from the JSON file
    if not os.path.exists(json_file):
        print(f"No news data found in {json_file}.")
        return

    try:
        with open(json_file, "r") as file:
            news_data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {json_file}. Please check the file's content.")
        return

    # Current time for comparison
    now = datetime.now()

    # Filter the news
    updated_news_data = []
    for news in news_data:
        # Check if the news is unsent and send it
        if not news.get("sentToChannel", False):
            message = f"{news['title']}\n\nSource: {news['source']}"
            sent = send_to_telegram(message, BOT_API_TOKEN, CHANNEL_ID)

            if sent:
                news["sentToChannel"] = True

        # Check the timestamp and keep news within 24 hours
        try:
            news_timestamp = datetime.fromisoformat(news.get("timestamp", now.isoformat()))
        except ValueError:
            # If the timestamp is invalid, use current time as fallback
            print(f"Invalid timestamp for news: {news.get('title')}. Using current time.")
            news_timestamp = now

        if now - news_timestamp < timedelta(hours=24):
            updated_news_data.append(news)

    # Save the updated news data back to the JSON file
    with open(json_file, "w") as file:
        json.dump(updated_news_data, file, indent=4)

    print("All unsent news has been processed and old news removed.")


send_unsent_news()
