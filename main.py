import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
import os
import asyncio

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents definieren
intents = Intents.default()
intents.message_content = True
intents.members = True  # Für Mitgliederinformationen

# Bot erstellen
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    help_command=None  # Eigenes Help-System
)

# Cog-Liste
COGS = ["cogs.olddb", "cogs.control", "cogs.alliance"]

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    # Slash Commands syncen
    synced = await bot.tree.sync()
    print(f"🔄 Synced {len(synced)} slash commands!")

async def main():
    await load_cogs()
    await bot.start(TOKEN)

# asyncio-Event-Loop starten
asyncio.run(main())
