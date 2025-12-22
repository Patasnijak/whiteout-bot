from discord import app_commands
from discord.ext import commands

class Alliance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="alliance_info", description="Zeigt Informationen über eine Allianz")
    async def alliance_info(self, interaction, alliance_name: str):
        # Hier kannst du DB-Logik einfügen
        await interaction.response.send_message(f"Informationen zur Allianz `{alliance_name}`: ...")

async def setup(bot: commands.Bot):
    await bot.add_cog(Alliance(bot))

