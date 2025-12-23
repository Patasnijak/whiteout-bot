import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file!")

# Intents setup
intents = discord.Intents.default()
intents.message_content = True  # für Commands und Events

# Bot setup
bot = commands.Bot(command_prefix="/", intents=intents)

# Async function to load all cogs
async def load_all_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash comman
