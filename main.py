import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.members = True  # falls du Mitgliederdaten brauchst

# Bot Setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Funktion zum Laden der Cogs
async def load_all_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# On Ready Event
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    await load_all_cogs()
    # Sync Slash Commands
    synced = await bot.tree.sync()
    print(f"🔄 Synced {len(synced)} slash commands!")

# Run the bot
bot.run(TOKEN)
