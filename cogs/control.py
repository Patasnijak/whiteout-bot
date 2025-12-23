import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import os

DB_PATH = "db/wos.db"

class Control(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init_db()

    def init_db(self):
        os.makedirs("db", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    fid = app_commands.Group(
        name="fid",
        description="F-ID Verwaltung"
    )

    @fid.command(name="add", description="F-ID hinzufügen")
    @app_commands.describe(
        fid="Die Spieler-FID",
        name="Name des Spielers"
    )
    async def fid_add(
        self,
        interaction: discord.Interaction,
        fid: int,
        name: str
    ):
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR REPLACE INTO players (fid, name) VALUES (?, ?)",
            (fid, name)
        )
        conn.commit()
        conn.close()

        await interaction.response.send_message(
            f"✅ FID **{fid}** für **{name}** gespeichert.",
            ephemeral=True
        )

    @fid.command(name="list", description="Alle gespeicherten F-IDs anzeigen")
    async def fid_list(self, interaction: discord.Interaction):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT fid, name FROM players ORDER BY fid")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await interaction.response.send_message(
                "ℹ️ Keine F-IDs gespeichert.",
                ephemeral=True
            )
            return

        msg = "\n".join([f"• `{fid}` → **{name}**" for fid, name in rows])

        await interaction.response.send_message(
            f"📋 **Gespeicherte Spieler:**\n{msg}",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Control(bot))
