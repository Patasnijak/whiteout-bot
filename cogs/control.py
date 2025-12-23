import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import sqlite3
import time
import hashlib
import os

# Wenn du die experimental API nutzt, brauchst du oft einen "secret" key.
# Viele WoS reverse-engineered Tools nutzen diesen in Anfragen.
# Standard ist leer — du kannst ihn später anpassen.
API_SECRET = os.getenv("WOS_API_SECRET", "")

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/players.sqlite"
        self.ensure_db()

    def ensure_db(self):
        os.makedirs("db", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid INTEGER PRIMARY KEY,
                name TEXT,
                furnace_level INTEGER
            )
        """)
        conn.commit()
        conn.close()

    async def fetch_from_api(self, fid: int):
        """
        Experimenteller API‑Call.
        Versucht mit Giftcode-API Daten zu holen.
        """
        # Endpoint, der in der Community als experimentell beschrieben ist
        url = "https://wos-giftcode-api.centurygame.com/api/player"

        # Zeit und Sign generieren
        t = int(time.time() * 1000)
        form_str = f"fid={fid}&time={t}"
        sign = hashlib.md5((form_str + API_SECRET).encode()).hexdigest()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data={"sign": sign, "fid": fid, "time": t}) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
            except Exception as e:
                print(f"[WOS API] Request Failed: {e}")
                return None

    @app_commands.command(name="fid_add", description="Experimentell alle Daten zu einer FID abrufen und speichern")
    @app_commands.describe(fid="Die Spieler FID")
    async def fid_add(self, interaction: discord.Interaction, fid: int):
        await interaction.response.defer(ephemeral=True)

        # API Daten holen
        data = await self.fetch_from_api(fid)

        # Wenn die API nichts zurückgibt → fallback
        if not data:
            await interaction.followup.send(f"❌ Keine Daten von der API für FID `{fid}`.")
            return

        # Versuchen aus Antwort Werte zu holen
        name = data.get("nickname") or data.get("name") or "Unbekannt"
        furnace = data.get("furnace_lv") or data.get("furnaceLevel") or 0

        # In SQLite speichern
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO players (fid, name, furnace_level)
            VALUES (?, ?, ?)
        """, (fid, name, furnace))
        conn.commit()
        conn.close()

        await interaction.followup.send(
            f"✅ FID `{fid}` gespeichert!\n"
            f"• Name: `{name}`\n"
            f"• Furnace Level: `{furnace}`"
        )

async def setup(bot):
    await bot.add_cog(Control(bot))
