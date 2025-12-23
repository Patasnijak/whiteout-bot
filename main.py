import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

async def load_all_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def main():
    await load_all_cogs()
    await bot.start(TOKEN)

# Run the bot
asyncio.run(main())
