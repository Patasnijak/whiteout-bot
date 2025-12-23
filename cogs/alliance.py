import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/players.sqlite"

    @app_commands.command(name="alliance_list", description="Zeigt alle Spieler einer Allianz")
    @app_commands.describe(alliance="Name der Allianz")
    async def alliance_list(self, interaction: discord.Interaction, alliance: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fid, name, furnace_level FROM players WHERE alliance=?", (alliance,))
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            await interaction.response.send_message(f"Keine Spieler in der Allianz `{alliance}` gefunden.")
            return
        msg = "\n".join([f"{name} (FID {fid}, Level {furnace})" for fid, name, furnace in rows])
        await interaction.response.send_message(f"**Spieler in {alliance}:**\n{msg}")

async def setup(bot):
    await bot.add_cog(Alliance(bot))
