import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = ["olddb", "control", "alliance"]

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    print("🔄 Syncing slash commands...")
    await bot.tree.sync()
    print("✅ Slash commands synced!")

async def main():
    await load_cogs()

    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN fehlt als Environment Variable")

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
