# Web Scraper Telegram Bot

This project is a cryptocurrency news scraper that uses **BeautifulSoup (bs4)** to scrape news related to cryptocurrencies. It then sends the latest updates to a **Telegram channel** using a **Telegram Bot**.

## Features

- Scrapes cryptocurrency-related news from a specified website.
- Sends the latest news updates to a Telegram channel using a Telegram bot.
- Adds a timestamp to the scraped news and saves it in a JSON file for future reference.

## Technologies Used

- **Python**: The programming language used for the scraper and the bot.
- **BeautifulSoup (bs4)**: Used to parse and extract data from the HTML content of the webpage.
- **Requests**: Fetches the HTML content of the webpage.
- **JSON**: Stores scraped news data with a timestamp.

## Installation

Follow these steps to get your project up and running locally:

### 1. Clone the repository

Clone the project to your local machine using Git:

```bash
git clone https://github.com/your-username/web_scraper_telegram_bot.git
cd web_scraper_telegram_bot
```

### 2. Install the required dependencies

Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```
### 3. Set up environment variables

Create a `.env` file in the root directory of the project and add your **Telegram Bot API token** and **Channel ID**:

```env
BOT_API_TOKEN=your-telegram-bot-api-token
CHANNEL_ID=your-channel-id
```


