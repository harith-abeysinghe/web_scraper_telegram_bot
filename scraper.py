import os
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime  # Import datetime module

def read_json_file(json_file):
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                return []
    return []


def write_json_file(json_file, data):
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the current date and time

def get_news_by_topic_cryptoNews(topic: str, num_articles: int = 10, json_file: str = "news_data.json"):
    URL = f"https://cryptonews.net/news/{topic}/"
    r = requests.get(URL)

    if r.status_code != 200:
        print(f"Failed to retrieve news for topic: {topic}")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    news_all = soup.find_all("div", {"class": "row news-item start-xs"})

    existing_news = read_json_file(json_file)
    existing_titles = {news["title"] for news in existing_news}

    new_entries = []

    for news in news_all[:num_articles]:
        title_tag = news.find("a", {"class": "title"})
        if title_tag:
            title = title_tag.get_text(strip=True)

            if title in existing_titles:
                continue

            href = title_tag.get("href")
            source = f"https://cryptonews.net{href}" if href else "No source available"

            new_entry = {
                "title": title,
                "source": source,
                "timestamp": get_current_timestamp(),  # Add the timestamp
                "sentToChannel": False
            }
            new_entries.append(new_entry)

    existing_news.extend(new_entries)
    write_json_file(json_file, existing_news)

    print(f"Added {len(new_entries)} new articles to {json_file}.")

def get_news_coinDesk(topic, num_articles: int = 10, json_file: str = "news_data.json"):
    URL = f"https://www.coindesk.com/{topic}"
    r = requests.get(URL)
    if r.status_code != 200:
        print(f"Failed to retrieve news")
        return False

    soup = BeautifulSoup(r.text, "html.parser")
    news_all = soup.find_all("div", {"class": "flex flex-col"})

    # Load existing data and track titles to avoid duplicates
    existing_news = read_json_file(json_file)
    existing_titles = {news["title"] for news in existing_news}

    new_entries = []

    for news in news_all[:num_articles]:
        a_tag = news.find("a", {"class": "text-color-charcoal-900 mb-4 hover:underline"})
        if a_tag:
            h3_tag = a_tag.find("h3")
            if h3_tag:
                title = h3_tag.get_text(strip=True)

                if title in existing_titles:
                    continue

                href = a_tag.get("href")  # Extract the href attribute
                source = f"https://www.coindesk.com{href}" if href else "No source available"

                new_entry = {
                    "title": title,
                    "source": source,
                    "timestamp": get_current_timestamp(),  # Add the timestamp
                    "sentToChannel": False
                }
                new_entries.append(new_entry)

    existing_news.extend(new_entries)
    write_json_file(json_file, existing_news)

    print(f"Added {len(new_entries)} new articles to {json_file}.")


topics_cryptoNews = ["bitcoin", "ethereum", "altcoins"]

for topic in topics_cryptoNews:
    get_news_by_topic_cryptoNews(topic)

topics_coinDesk = ["markets", "tech"]

for topic in topics_coinDesk:
    get_news_coinDesk(topic)
