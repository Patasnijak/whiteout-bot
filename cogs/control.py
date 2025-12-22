from discord.ext import commands

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Test command for bot")
    async def ping(self, ctx):
        await ctx.respond("Pong! ✅")

def setup(bot):
    bot.add_cog(Control(bot))

