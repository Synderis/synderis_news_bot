# Synderis News Bot

Synderis News Bot is a Discord bot that scrapes various news articles and posts them to their respective channels daily. This bot is designed to keep your community updated with the latest news.

## Features

- Scrapes news articles from various sources.
- Reads the last 50 messages to see if the news article has already been posted.
- Posts news articles to specified Discord channels if the article was created today.
- Easy to configure and extend.

## Requirements

- Python 3.12
- Discord Token and Channel Mapping in AWS Secrets Manager

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/synderis_news_bot.git
    cd synderis_news_bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the bot:
```sh
python main.py
```

The bot will post a message if it finds an article posted that day if it isn't found in the last 50 messages of the channel.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
