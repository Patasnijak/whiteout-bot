import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /setprefix
    @app_commands.command(name="setprefix", description="Setze ein neues Bot-Prefix für den Server")
    async def setprefix(self, interaction: discord.Interaction, prefix: str):
        db_path = "db/control.sqlite"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR REPLACE INTO settings (guild_id, prefix) VALUES (?, ?)", (interaction.guild.id, prefix))
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"✅ Prefix wurde auf `{prefix}` gesetzt!")

async def setup(bot):
    await bot.add_cog(Control(bot))
