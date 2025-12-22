import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Zeigt alle verfügbaren Befehle an")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🤖 Befehlsübersicht", color=discord.Color.blue())
        for command in self.bot.tree.walk_commands():
            if not command.parent:  # Nur Hauptbefehle
                name = f"/{command.name}"
                desc = command.description or "Keine Beschreibung"
                embed.add_field(name=name, value=desc, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
