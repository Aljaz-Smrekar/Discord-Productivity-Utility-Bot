import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import asyncio

from services.database import Database


load_dotenv()  # Loads variables from .env
token = os.getenv("DISCORD_TOKEN")


logging.basicConfig(
    # level=logging.DEBUG,  # Change to INFO in production and keep DEBUG for development
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w"),
        logging.StreamHandler()  # prints to console as well
    ]
)

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
intents.members = True  # Needed to access member information


bot = commands.Bot(command_prefix="!", intents=intents)

async def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

# Run it before starting the bot
async def main():
    async with bot:
        await load_all_cogs()
        await bot.start(token)

asyncio.run(main())

    