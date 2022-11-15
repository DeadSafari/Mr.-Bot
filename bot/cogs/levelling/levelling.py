import discord
from discord.ext import commands

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.levelling.Levelling is now ready!")

async def setup(bot):
    await bot.add_cog(Levelling(bot))