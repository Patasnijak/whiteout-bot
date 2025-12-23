import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import sqlite3

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # SQLite DB Pfad anpassen
        self.db_path = "db/alliance.db"

    async def add_to_db(self, fid, name, level, alliance):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Tabelle erstellen, falls nicht vorhanden
        c.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid INTEGER PRIMARY KEY,
                name TEXT,
                level INTEGER,
                alliance TEXT
            )
        """)
        # Spieler einfügen oder updaten
        c.execute("""
            INSERT INTO players(fid, name, level, alliance)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(fid) DO UPDATE SET
                name=excluded.name,
                level=excluded.level,
                alliance=excluded.alliance
        """, (fid, name, level, alliance))
        conn.commit()
        conn.close()

    @app_commands.command(name="fid_add", description="Spieler automatisch hinzufügen")
    @app_commands.describe(fid="FID des Spielers")
    async def fid_add(self, interaction: discord.Interaction, fid: int):
        await interaction.response.defer()  # kurz warten, während API geholt wird

        # API-URL anpassen, wenn nötig
        url = f"https://api.whiteoutsurvival.com/player/{fid}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await interaction.followup.send(f"❌ Fehler beim Abrufen von FID {fid}. Status: {resp.status}")
                    return
                data = await resp.json()

        # Daten extrahieren
        try:
            name = data["name"]
            level = data["level"]
            alliance = data["alliance"]
        except KeyError:
            await interaction.followup.send("❌ Ungültige API-Antwort.")
            return

        # In DB speichern
        await self.add_to_db(fid, name, level, alliance)

        await interaction.followup.send(f"✅ Spieler **{name}** (Level {level}) in Allianz **{alliance}** hinzugefügt.")

async def setup(bot):
    await bot.add_cog(Control(bot))
