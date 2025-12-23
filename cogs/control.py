import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import sqlite3
import time
import hashlib
import os

# Optional: Experimenteller Secret-Key (falls nötig)
API_SECRET = os.getenv("WOS_API_SECRET", "")

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/players.sqlite"
        self.ensure_db()

    def ensure_db(self):
        # Erstellt DB, wenn nicht existiert
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
        Experimentelle API‑Abfrage über Giftcode‑Endpoint.
        Rückgabe ist JSON oder None.
        """
        url = "https://wos-giftcode-api.centurygame.com/api/player"
        t = int(time.time() * 1000)
        form_str = f"fid={fid}&time={t}"
        sign = hashlib.md5((form_str + API_SECRET).encode()).hexdigest()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data={"sign": sign, "fid": fid, "time": t}) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except Exception:
            return None

    @app_commands.command(name="fid_add", description="Spieler anhand FID automatisch holen und speichern")
    @app_commands.describe(fid="FID des Spielers")
    async def fid_add(self, interaction: discord.Interaction, fid: int):
        await interaction.response.defer(ephemeral=True)

        # API‑Abfrage
        data = await self.fetch_from_api(fid)

        # Wenn keine Antwort
        if not data:
            await interaction.followup.send(f"❌ Keine Daten von der API für FID `{fid}` gefunden.")
            return

        # Name & Furnace Level aus Antwort versuchen
        # Unterschiedliche Keys möglich je nach Endpunkt: nickname, name, playerName, furnace_lv ...
        name = data.get("nickname") or data.get("name") or data.get("playerName") or "Unbekannt"
        furnace = (
            data.get("furnace_lv") or
            data.get("furnaceLevel") or
            data.get("furnace") or
            0
        )

        # Speichern in DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO players (fid, name, furnace_level)
            VALUES (?, ?, ?)
        """, (fid, name, furnace))
        conn.commit()
        conn.close()

        await interaction.followup.send(
            f"✅ Daten für FID `{fid}` gespeichert:\n"
            f"• **Name:** {name}\n"
            f"• **Furnace Level:** {furnace}"
        )

async def setup(bot):
    await bot.add_cog(Control(bot))
