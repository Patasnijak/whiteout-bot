from discord import app_commands, Interaction
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Zeigt alle Befehle des Bots an")
    async def help(self, interaction: Interaction):
        embed = discord.Embed(
            title="Whiteout Bot Commands",
            description="Liste aller Slash-Commands",
            color=0x00ff00
        )

        for cog_name, cog in self.bot.cogs.items():
            commands_list = []
            for cmd in self.bot.tree.get_commands():  # Alle Slash-Commands
                if cmd.cog_name == cog_name:
                    commands_list.append(f"/{cmd.name} - {cmd.description}")
            if commands_list:
                embed.add_field(name=cog_name, value="\n".join(commands_list), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
