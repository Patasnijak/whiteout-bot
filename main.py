import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot initialisieren
bot = commands.Bot(command_prefix="/", intents=intents)

# Funktion zum Laden der Cogs
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# Event: Bot ist ready
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    # Slash-Commands synchronisieren
    synced = await bot.tree.sync()
    print(f"🔄 Synced {len(synced)} slash commands!")

# Hauptfunktion
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# Starten
asyncio.run(main())
