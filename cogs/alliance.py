from discord import app_commands
from discord.ext import commands
import sqlite3

class Alliance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn_alliance = sqlite3.connect("db/alliance.sqlite")

    @app_commands.command(name="alliance_info", description="Zeigt Informationen über eine Allianz")
    @app_commands.describe(alliance_id="ID der Allianz")
    async def alliance_info(self, interaction, alliance_id: int):
        cursor = self.conn_alliance.cursor()
        cursor.execute("SELECT name, channel_id, interval FROM alliancesettings WHERE alliance_id=?", (alliance_id,))
        data = cursor.fetchone()
        if not data:
            await interaction.response.send_message("Allianz nicht gefunden.")
            return
        await interaction.response.send_message(f"**Allianz ID:** {alliance_id}\nName: {data[0]}\nChannel: {data[1]}\nInterval: {data[2]}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Alliance(bot))
))

