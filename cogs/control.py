from discord.ext import commands
from discord import app_commands

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Test command")
    async def ping(self, interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="restart", description="Restart the bot (admin only)")
    async def restart(self, interaction):
        # Optional: hier Admin-Prüfung einfügen
        await interaction.response.send_message("Bot wird neu gestartet...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Control(bot))
