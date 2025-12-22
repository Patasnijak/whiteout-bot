from discord import app_commands
from discord.ext import commands

class Control(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="restart_bot", description="Startet den Bot neu")
    async def restart_bot(self, interaction):
        await interaction.response.send_message("Bot wird neu gestartet...")
        await self.bot.close()  # Schließt den Bot, Hauptscript kann Neustart handhaben

    @app_commands.command(name="ping", description="Prüft die Latenz des Bots")
    async def ping(self, interaction):
        await interaction.response.send_message(f"Pong! Latenz: {round(self.bot.latency*1000)}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Control(bot))


