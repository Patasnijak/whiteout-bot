import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import sqlite3
import time
import hashlib
import os

# 🚧 EXPERIMENTELLER SECRET KEY (falls nötig)
# Du kannst ihn in Railway als Environment Variable setzen:
# z.B. WOS_API_SECRET=abcdef…
API_SECRET = os.getenv("WOS_API_SECRET", "")

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/players.sqlite"
        self.ensure_db()

    def ensure_db(self):
        """Stellt sicher, dass die DB und die Tabelle existieren."""
        os.makedirs("db", exist_ok=True)
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
        """
        Holt Spielerdaten über den experimentellen API‑Endpoint.
        Liefert None, wenn Fehler oder keine Daten.
        """
        url = "https://wos-giftcode-api.centurygame.com/api/player"

        # Signatur: md5("fid=…&time=…" + secret)
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
    @app_commands.describe(fid="Die Spieler‑FID")
    async def fid_add(self, interaction: discord.Interaction, fid: int):
        # Zeige Loading‑Hinweis
        await interaction.response.defer(ephemeral=True)

        # API abfragen
        data = await self.fetch_from_api(fid)
        if not data:
            await interaction.followup.send(
                f"❌ Konnte keine Daten für FID `{fid}` abrufen.",
                ephemeral=True
            )
            return

        # Versuche Felder zu lesen (Fallbacks)
        name = data.get("nickname") or data.get("name") or data.get("playerName") or "Unbekannt"
        furnace = (
            data.get("furnace_lv") or
            data.get("furnaceLevel") or
            data.get("furnace") or
            0
        )
        alliance = data.get("alliance") or data.get("allianceName") or "Keine Allianz"

        # Daten speichern
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO players (fid, name, furnace_level, alliance)
            VALUES (?, ?, ?, ?)
        """, (fid, name, furnace, alliance))
        conn.commit()
        conn.close()

        # Ergebnis ausgeben
        await interaction.followup.send(
            f"✅ **Spielerdaten gespeichert:**\n"
            f"• **FID:** {fid}\n"
            f"• **Name:** {name}\n"
            f"• **Furnace Level:** {furnace}\n"
            f"• **Allianz:** {alliance}",
            ephemeral=True
        )

async def setup(bot):
    bot.add_cog(Control(bot))  # ⚠ kein await!
