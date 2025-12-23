import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio

# Token laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot-Objekt
bot = commands.Bot(command_prefix="!", intents=intents)

# Asynchron Cogs laden
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"🤖 Logged in als {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"Fehler beim Sync: {e}")

# Entry Point
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
