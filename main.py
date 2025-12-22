
import discord
from discord.ext import commands
import os
import sqlite3
import asyncio
from colorama import Fore as F, Style as R, init

init(autoreset=True)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

if not os.path.exists("db"):
    os.makedirs("db")
databases = {
    "conn_alliance": "db/alliance.sqlite",
    "conn_giftcode": "db/giftcode.sqlite",
    "conn_changes": "db/changes.sqlite",
    "conn_users": "db/users.sqlite",
    "conn_settings": "db/settings.sqlite",
}
connections = {name: sqlite3.connect(path) for name, path in databases.items()}

def create_tables():
    with connections["conn_changes"] as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS nickname_changes (id INTEGER PRIMARY KEY AUTOINCREMENT, fid INTEGER, old_nickname TEXT, new_nickname TEXT, change_date TEXT)")
    with connections["conn_users"] as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (fid INTEGER PRIMARY KEY, nickname TEXT, furnace_lv INTEGER DEFAULT 0, kid INTEGER, stove_lv_content TEXT, alliance TEXT)")

create_tables()

async def load_cogs():
    cogs = ["olddb", "control", "alliance"]  # Nur die 3 Cogs, die du hast
    failed_cogs = []

    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"✓ Loaded cog: {cog}")
        except Exception as e:
            print(f"✗ Failed to load cog {cog}: {e}")
            failed_cogs.append(cog)

    if failed_cogs:
        print(f"\n⚠️ {len(failed_cogs)} cog(s) failed to load: {', '.join(failed_cogs)}")
        print("The bot will continue with reduced functionality.")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


async def main():
    print("Bot starting...")
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("ERROR: DISCORD_TOKEN not set")
        while True:
            await asyncio.sleep(60)

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
