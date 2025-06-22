import requests
import scraper
import boto3
import json

def get_secret(secret_name, region_name="us-east-2"):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Load secrets from AWS Secrets Manager
secrets = get_secret('synderis-news-bot')
discord_token = secrets.get('discord_token')
discord_channels = secrets.get('discord_channels')

link_dict = {
    'league': ['https://www.riotgames.com/en/news'],
    'osrs': ['https://secure.runescape.com/m=news/archive?oldschool=1'],
    'mtg': ['https://magic.wizards.com/en/news'],
    'wow': ['https://worldofwarcraft.blizzard.com/en-us/news'],
    'brighter_shores': ['https://brightershores.pro/category/news']
}

def parse_channels(channels_env):
    mapping = {}
    for entry in channels_env.split(','):
        if ':' in entry:
            tag, chan_id = entry.split(':', 1)
            mapping[tag.strip()] = int(chan_id.strip())
    return mapping

def send_discord_message(channel_id, content):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {discord_token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": content
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Sending message to channel {channel_id}: {content}")
    print(f"Response status code: {response.status_code}")
    if response.status_code != 200 and response.status_code != 204:
        print(f"Discord API error response: {response.text}")
    return response.status_code == 200 or response.status_code == 204

def check_discord_messages(channel_id, news_list):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100"
    headers = {
        "Authorization": f"Bot {discord_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch messages: {response.status_code} {response.text}")
        return None
    messages = response.json()
    existing_urls = set()
    for msg in messages:
        # Check message content
        if msg.get("content") in news_list:
            existing_urls.add(msg.get("content"))
        # Check embeds for url field
        for embed in msg.get("embeds", []):
            embed_url = embed.get("url")
            if embed_url in news_list:
                existing_urls.add(embed_url)
    # Return only URLs that have NOT been posted yet
    return [url for url in news_list if url not in existing_urls]

def lambda_handler(event, context):
    print("Starting news scraper...")
    channel_map = parse_channels(discord_channels)
    print(f"Channel mapping: {channel_map}")
    for key, value in link_dict.items():
        channel_id = channel_map.get(key)
        print(f"Processing {key} with URL {value[0]} and channel ID {channel_id}")
        exit(0)
        if not channel_id:
            print(f"No channel ID found for {key}, skipping.")
            continue
        news = scraper.get_news(key, value[0])
        if news:
            print(f'Got news: {news}')
            # Only get new URLs that haven't been posted yet
            new_urls = check_discord_messages(channel_id, news)
            if not new_urls:
                print(f"No new news items found for {key}.")
                continue
            for item in new_urls:
                print(f"Found new news item: {item}")
                send_discord_message(channel_id, item)
                print(f"Sent news item to channel {channel_id}: {item}")
    return {"status": "done"}