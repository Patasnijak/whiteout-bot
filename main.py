import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents einstellen
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# Bot-Objekt erstellen
bot = commands.Bot(command_prefix="/", intents=intents)

# Funktion zum Laden aller Cogs
async def load_cogs():
    cogs = ["olddb", "control", "alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# Event beim Starten des Bots
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    # Slash-Commands synchronisieren
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

# Startet den Bot
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# asyncio.run für asynchrone main()
import asyncio
asyncio.run(main())
