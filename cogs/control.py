from discord import app_commands
from discord.ext import commands

class Control(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Zeigt die Latenz des Bots an")
    async def ping(self, interaction):
        await interaction.response.send_message(f"Pong! Latenz: {round(self.bot.latency*1000)}ms")

    @app_commands.command(name="restart", description="Startet den Bot neu")
    async def restart(self, interaction):
        await interaction.response.send_message("Bot wird neu gestartet...")
        await self.bot.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Control(bot))
