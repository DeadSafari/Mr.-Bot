import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.economy.Economy is now ready!")

async def setup(bot):
    bot.add_cog(Economy(bot))