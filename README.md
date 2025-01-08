# Synderis News Bot

Synderis News Bot is a Discord bot that scrapes various news articles and posts them to their respective channels daily. This bot is designed to keep your community updated with the latest news.

## Features

- Scrapes news articles from various sources.
- Posts news articles to specified Discord channels daily at a set time.
- Easy to configure and extend.

## Requirements

- Python 3.8+
- `discord.py` library
- `python-dotenv` library

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

3. Create a `.env` file in the root directory and add your Discord bot token:
    ```env
    DISCORD_TOKEN=your_bot_token_here
    ```

4. Update the `CHANNEL_ID` in `main.py` with the ID of the channel you want the bot to post in.

## Usage

Run the bot:
```sh
python main.py
```

The bot will post a daily message at the specified time in the specified channel.

## Configuration

- **BOT_TOKEN**: Your Discord bot token. Set this in the `.env` file.
- **CHANNEL_ID**: The ID of the Discord channel where the bot will post messages.
- **POST_TIME**: The time of day when the bot will post the message (24-hour format).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
