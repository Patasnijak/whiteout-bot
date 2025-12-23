# main.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Lade die .env Datei
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setzen
intents = discord.Intents.default()
intents.message_content = True  # nötig für Text-Commands
intents.members = True          # nötig für Member-bezogene Events

# Bot-Instanz
bot = commands.Bot(command_prefix="/", intents=intents)

# Funktion zum Laden aller Cogs
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

# Event: Bot bereit
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    # Slash-Commands synchronisieren
    synced = await bot.tree.sync()
    print(f"🔄 Synced {len(synced)} slash commands!")

# Start-Funktion
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# Python 3.11+ kompatibel
asyncio.run(main())
