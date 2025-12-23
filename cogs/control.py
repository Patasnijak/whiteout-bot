import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

DB_PATH = "db/fids.db"

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fid_add", description="Füge einem User eine Whiteout FID hinzu")
    @app_commands.describe(member="Discord User", fid="Whiteout Survival FID")
    async def fid_add(self, interaction: discord.Interaction, member: discord.Member, fid: int):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Nur Admins dürfen diesen Command nutzen.",
                ephemeral=True
            )
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO fids (guild_id, discord_id, fid, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            interaction.guild.id,
            member.id,
            fid,
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

        await interaction.response.send_message(
            f"✅ **FID gespeichert**\nUser: {member.mention}\nFID: `{fid}`",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Control(bot))
