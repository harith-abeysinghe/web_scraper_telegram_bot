import requests
from bs4 import BeautifulSoup


def get_news_by_topic(topic: str, num_articles: int = 10):
    URL = f"https://cryptonews.net/news/{topic}/"
    r = requests.get(URL)

    if r.status_code != 200:
        print(f"Failed to retrieve news for topic: {topic}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    news_all = soup.find_all("div", {"class": "row news-item start-xs"})

    for news in news_all[:num_articles]:
        title_tag = news.find("a", {"class": "title"})
        if title_tag:
            title = title_tag.get_text(strip=True)

            href = title_tag.get("href")
            source = f"https://cryptonews.net{href}" if href else "No source available"

            print(f"Title: {title}")
            print(f"Source: {source}")
            print()


get_news_by_topic("bitcoin", 10)
