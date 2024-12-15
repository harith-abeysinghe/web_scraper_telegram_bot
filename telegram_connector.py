import json

import requests
import os
from dotenv import load_dotenv

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

    with open(json_file, "r") as file:
        news_data = json.load(file)

    for news in news_data:
        if not news.get("sentToChannel"):
            message = f"{news['title']}\n\nSource: {news['source']}"
            sent = send_to_telegram(message, BOT_API_TOKEN, CHANNEL_ID)

            if sent:
                news["sentToChannel"] = True

    # Save the updated news data back to the JSON file
    with open(json_file, "w") as file:
        json.dump(news_data, file, indent=4)

    print("All unsent news has been processed.")

send_unsent_news()