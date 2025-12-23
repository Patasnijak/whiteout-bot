import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from datetime import datetime

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /alliance add
    @app_commands.command(name="alliance_add", description="Füge einen Spieler zur Allianz hinzu")
    async def alliance_add(self, interaction: discord.Interaction, fid: int, username: str, alliance: str):
        db_path = "db/alliance.sqlite"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT OR REPLACE INTO alliance_members (fid, username, alliance, last_seen) VALUES (?, ?, ?, ?)",
                       (fid, username, alliance, now))
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"✅ Spieler {username} wurde der Allianz {alliance} hinzugefügt!")

async def setup(bot):
    await bot.add_cog(Alliance(bot))
