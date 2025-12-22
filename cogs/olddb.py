from discord.ext import commands
from discord import app_commands

class OldDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check_user", description="Check a user's stats in the database")
    async def check_user(self, interaction, user_id: int):
        # Hier kannst du DB-Abfragen einfügen
        await interaction.response.send_message(f"Checking data for user ID: {user_id}")

async def setup(bot):
    await bot.add_cog(OldDB(bot))

