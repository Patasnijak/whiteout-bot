import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import os

class OldDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /fid add
    @app_commands.command(name="fid_add", description="Füge einen Spieler hinzu")
    async def fid_add(self, interaction: discord.Interaction, fid: int, username: str, level: int):
        db_path = "db/olddb.sqlite"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR REPLACE INTO users (fid, username, level) VALUES (?, ?, ?)", (fid, username, level))
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"✅ Spieler {username} (FID: {fid}, Level: {level}) wurde hinzugefügt!")

async def setup(bot):
    await bot.add_cog(OldDB(bot))
