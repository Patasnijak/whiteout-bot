from discord import app_commands
from discord.ext import commands

class OldDB(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_old_users", description="Zeigt alte Benutzer aus der Datenbank an")
    async def show_old_users(self, interaction):
        # Hier kannst du die Logik einfügen, um alte Benutzer zu laden
        await interaction.response.send_message("Liste der alten Benutzer: ...")

async def setup(bot: commands.Bot):
    await bot.add_cog(OldDB(bot))
))
