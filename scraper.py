import os
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dotenv import load_dotenv
from db_connection import connect_to_mongodb  # Importing from the new db_connection.py

# Connect to MongoDB
collection = connect_to_mongodb()

# Get the current timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insert news into MongoDB
def insert_news_into_db(news_list):
    for news in news_list:
        if not collection.find_one({"title": news["title"]}):  # Check for duplicates
            collection.insert_one(news)

def get_news_by_topic_cryptoNews(topic: str, num_articles: int = 10):
    URL = f"https://cryptonews.net/news/{topic}/"
    r = requests.get(URL)

    if r.status_code != 200:
        print(f"Failed to retrieve news for topic: {topic}")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    news_all = soup.find_all("div", {"class": "row news-item start-xs"})

    new_entries = []

    for news in news_all[:num_articles]:
        title_tag = news.find("a", {"class": "title"})
        if title_tag:
            title = title_tag.get_text(strip=True)

            if collection.find_one({"title": title}):  # Check for duplicates in MongoDB
                continue

            href = title_tag.get("href")
            source = f"https://cryptonews.net{href}" if href else "No source available"

            new_entry = {
                "title": title,
                "source": source,
                "timestamp": get_current_timestamp(),
                "sentToChannel": False
            }
            new_entries.append(new_entry)

    insert_news_into_db(new_entries)
    print(f"Added {len(new_entries)} new articles for topic '{topic}' to MongoDB.")

def get_news_coinDesk(topic, num_articles: int = 10):
    URL = f"https://www.coindesk.com/{topic}"
    r = requests.get(URL)
    if r.status_code != 200:
        print(f"Failed to retrieve news for topic: {topic}")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    news_all = soup.find_all("div", {"class": "flex flex-col"})

    new_entries = []

    for news in news_all[:num_articles]:
        a_tag = news.find("a", {"class": "text-color-charcoal-900 mb-4 hover:underline"})
        if a_tag:
            h3_tag = a_tag.find("h3")
            if h3_tag:
                title = h3_tag.get_text(strip=True)

                if collection.find_one({"title": title}):  # Check for duplicates in MongoDB
                    continue

                href = a_tag.get("href")  # Extract the href attribute
                source = f"https://www.coindesk.com{href}" if href else "No source available"

                new_entry = {
                    "title": title,
                    "source": source,
                    "timestamp": get_current_timestamp(),
                    "sentToChannel": False
                }
                new_entries.append(new_entry)

    insert_news_into_db(new_entries)
    print(f"Added {len(new_entries)} new articles for topic '{topic}' to MongoDB.")


# Scrape news for topics
topics_cryptoNews = ["bitcoin", "ethereum", "altcoins"]
for topic in topics_cryptoNews:
    get_news_by_topic_cryptoNews(topic)

topics_coinDesk = ["markets", "business"]
for topic in topics_coinDesk:
    get_news_coinDesk(topic)
