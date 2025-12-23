import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import aiohttp
import hashlib
import time

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# --- Whiteout API Helper ---
async def get_player_info(fid: int):
    secret = "DEIN_SECRET_KEY"
    t = int(time.time() * 1000)
    form_str = f"fid={fid}&time={t}"
    sign = hashlib.md5((form_str + secret).encode()).hexdigest()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://wos-giftcode-api.centurygame.com/api/player",
            data={"sign": sign, "fid": fid, "time": t}
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            return None

# --- Load Cogs ---
async def load_cogs():
    cogs = ["cogs.olddb", "cogs.control", "cogs.alliance"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

# --- Commands ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def fid(ctx, fid: int):
    data = await get_player_info(fid)
    if data:
        await ctx.send(f"Spielername: {data.get('nickname')}\nFurnace Level: {data.get('furnace_lv')}")
    else:
        await ctx.send("Spieler nicht gefunden oder API Fehler.")

# --- Startup ---
async def main():
    await load_cogs()
    await bot.start(TOKEN)

asyncio.run(main())
