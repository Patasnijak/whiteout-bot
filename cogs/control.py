import sqlite3
from discord import app_commands
from discord.ext import commands

DB_PATH = "db/players.db"  # Pfad zu deiner DB, passe ggf. an

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /fid add <ID>
    @app_commands.command(name="add", description="Füge eine Spieler-ID hinzu")
    @app_commands.describe(fid="Die Spieler-ID, die hinzugefügt werden soll")
    async def fid_add(self, interaction, fid: int):
        try:
            # Verbindung zur DB
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Tabelle erstellen, falls nicht existiert
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid INTEGER PRIMARY KEY,
                discord_id INTEGER
            )
            """)

            # Spieler-ID eintragen
            cursor.execute("INSERT OR REPLACE INTO players (fid, discord_id) VALUES (?, ?)", 
                           (fid, interaction.user.id))
            conn.commit()
            conn.close()

            await interaction.response.send_message(f"✅ Spieler-ID `{fid}` erfolgreich registriert für {interaction.user.mention}!")
        except Exception as e:
            await interaction.response.send_message(f"❌ Fehler beim Speichern der ID: {e}")

async def setup(bot):
    await bot.add_cog(Control(bot))
