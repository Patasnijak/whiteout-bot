from discord.ext import commands
from discord import app_commands

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="alliance_info", description="Get info about an alliance")
    async def alliance_info(self, interaction, alliance_name: str):
        # Hier kannst du DB-Abfragen einfügen
        await interaction.response.send_message(f"Info for alliance: {alliance_name}")

async def setup(bot):
    await bot.add_cog(Alliance(bot))

