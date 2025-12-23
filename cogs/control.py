import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import sqlite3
import time
import hashlib
import os
import asyncio

API_SECRET = os.getenv("WOS_API_SECRET", "")

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/players.sqlite"
        os.makedirs("db", exist_ok=True)
        self.ensure_db()
        self.track_names.start()

    def ensure_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid INTEGER PRIMARY KEY,
                name TEXT,
                furnace_level INTEGER,
                alliance TEXT
            )
        """)
        conn.commit()
        conn.close()

    async def fetch_from_api(self, fid: int):
        url = "https://wos-giftcode-api.centurygame.com/api/player"
        t = int(time.time() * 1000)
        form_str = f"fid={fid}&time={t}"
        sign = hashlib.md5((form_str + API_SECRET).encode()).hexdigest()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data={"sign": sign, "fid": fid, "time": t}, timeout=15) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except asyncio.TimeoutError:
            return None
        except Exception:
            return None

    @app_commands.command(name="fid_add", description="Hole Spielerdaten anhand FID und speichere sie.")
    @app_commands.describe(fid="Die Spieler-FID")
    async def fid_add(self, interaction: discord.Interaction, fid: int):
        await interaction.response.defer(ephemeral=True)
        data = await self.fetch_from_api(fid)
        if not data:
            await interaction.followup.send(f"❌ Konnte keine Daten für FID `{fid}` abrufen.", ephemeral=True)
            return
        name = data.get("nickname") or "Unbekannt"
        furnace = data.get("furnace_lv") or 0
        alliance = data.get("alliance") or "Keine Allianz"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO players (fid, name, furnace_level, alliance)
            VALUES (?, ?, ?, ?)
        """, (fid, name, furnace, alliance))
        conn.commit()
        conn.close()
        await interaction.followup.send(
            f"✅ **Spielerdaten gespeichert:**\n• **FID:** {fid}\n• **Name:** {name}\n• **Furnace Level:** {furnace}\n• **Allianz:** {alliance}",
            ephemeral=True
        )

    @tasks.loop(minutes=10)
    async def track_names(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fid, name FROM players")
        rows = cursor.fetchall()
        for fid, old_name in rows:
            data = await self.fetch_from_api(fid)
            if data:
                new_name = data.get("nickname") or old_name
                if new_name != old_name:
                    cursor.execute("UPDATE players SET name=? WHERE fid=?", (new_name, fid))
                    # Optional: Discord-Benachrichtigung an bestimmten Channel
                    # channel = self.bot.get_channel(DEIN_CHANNEL_ID)
                    # await channel.send(f"Spieler `{old_name}` hat seinen Namen zu `{new_name}` geändert!")
        conn.commit()
        conn.close()

async def setup(bot):
    await bot.add_cog(Control(bot))  # ✅ Korrekt: await
