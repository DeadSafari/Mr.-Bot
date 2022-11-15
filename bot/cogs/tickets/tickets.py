import discord
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.tickets.tickets is now ready!")

async def setup(bot):
    await bot.add_cog(Ticket(bot))