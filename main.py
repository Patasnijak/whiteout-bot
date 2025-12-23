import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot-Intents
intents = discord.Intents.default()
intents.message_content = True  # Falls du Nachrichten-Inhalte brauchst
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Alte Commands sauber entfernen
@bot.event
async def on_ready():
    # Alte globale Commands entfernen
    synced = await bot.tree.sync()
    print(f"✅ Bot ready! Logged in as {bot.user}")
    print(f"🔄 Synced {len(synced)} slash commands!")

# Funktion zum Laden aller Cogs
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except commands.CommandAlreadyRegistered:
            print(f"⚠ Command already registered in {cog}, skipping...")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# Hauptfunktion zum Starten
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# Run bot
asyncio.run(main())
