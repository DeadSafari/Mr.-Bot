from typing import Union
import discord
from discord.ext import commands

class giveawayFlags(commands.FlagConverter, case_insensitive=True):
    pass

class giveawayCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.Giveaway is now ready!")

    @commands.hybrid_command(
        name="gcreate",
        with_app_command=True,
        description="Creates a giveaway.",
        args=[]
    )
    async def _gcreate(
        self,
        ctx: Union[discord.Interaction, commands.Context],
        *,
        argss = None
    ):
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(giveawayCommands(bot))