import discord
from discord.ext import commands
import traceback
import json

class ErrorHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.events.Errors is now ready!")
    
    @commands.Cog.listener()
    async def on_error(self, error):
        print("we got here")
        print(error)
    
async def setup(bot):
    await bot.add_cog(ErrorHandlers(bot))