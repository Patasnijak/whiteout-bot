import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.members = True  # Für Member-bezogene Funktionen
bot = commands.Bot(command_prefix="/", intents=intents)

# ----------------------------
# Funktion zum Laden aller Cogs
# ----------------------------
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog.split('.')[-1]}")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}: {e}")

# ----------------------------
# Bot-Events
# ----------------------------
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Slash commands synchronisieren
        print(f"🔄 Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

# ----------------------------
# Main starten
# ----------------------------
async def main():
    await load_cogs()
    token = os.getenv("DISCORD_TOKEN")  # Token aus Railway/Environment Variable
    await bot.start(token)

# ----------------------------
# Script starten
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())
