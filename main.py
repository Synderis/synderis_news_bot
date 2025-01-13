import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
import os

import scraper

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Replace 'CHANNEL_ID' with the ID of the channel you want the bot to post in
CHANNEL_ID = 123456789012345678  # Replace with your channel ID
# Set the specific time you want the bot to post (24-hour format: HH:MM)
POST_TIME = time(12, 0)  # Example: 12:00 PM

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

link_dict = {'league': ['https://www.riotgames.com/en/news', 1],
    'osrs': ['https://secure.runescape.com/m=news/archive?oldschool=1', 2],
    'mtg': ['https://magic.wizards.com/en/news', 3],
    'wow': ['https://worldofwarcraft.blizzard.com/en-us/news', 4],
    'pokemon': ['https://www.pokemon.com/us/pokemon-news' , 5],
    'brighter_shores': ['https://brightershores.pro/category/news', 6],
    'poe': ['https://www.pathofexile.com/news', 7]}


async def wait_until(target_time):
    now = datetime.now()
    target_datetime = datetime.combine(now.date(), target_time)
    if now.time() > target_time:
        target_datetime += timedelta(days=1)  # Schedule for the next day
    wait_seconds = (target_datetime - now).total_seconds()
    await asyncio.sleep(wait_seconds)

async def send_daily_message():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await wait_until(POST_TIME)
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("Good day! Here's your daily message.")
        await asyncio.sleep(24 * 60 * 60)  # Wait for a day

async def deliver_daily_news():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await wait_until(POST_TIME)
        for key, value in link_dict.items():
            channel = bot.get_channel(value[1])
            news = await scraper.get_news(key,value[0])
            if news:
                for item in news:
                    await channel.send(item)
        await asyncio.sleep(24 * 60 * 60)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Start the background task
bot.loop.create_task(send_daily_message())

# Run the bot
bot.run(TOKEN)
