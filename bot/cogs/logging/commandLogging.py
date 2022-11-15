import discord
from discord.ext import commands

class commandLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.logging.CommandLogging is now ready!")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        commandInfo = {
            "name": ctx.command.name,
            "author": ctx.author.id,
            "prefix": ctx.prefix,
            "arguments": ctx.kwargs,
            "bot_permissions": ctx.bot_permissions
        }
        print(commandInfo)


async def setup(bot: commands.Bot):
    await bot.add_cog(commandLogging(bot))