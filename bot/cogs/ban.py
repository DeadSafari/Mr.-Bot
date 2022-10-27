#imports
import datetime
import json
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from typing import Union, Optional
from bot.functions.checkForPerms import checkForPerms
from bot.functions.formatString import formatString, formatString
from bot.functions.isEnabled import isEnabled
from bot.functions.isGloballyEnabled import isGloballyEnabled
from bot.functions.logToDb import logToDb
from bot.functions.returnLogsChannel import returnLogsChannel
from bot.functions.returnEmbedOrMessage import returnEmbedOrMessage

class banCommand(commands.Cog):
    def __init__(
        self,
        bot: Bot
    ):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("commands.Ban is now ready!")
    
    @commands.hybrid_command(
        name="ban",
        with_app_command=True,
        description="Bans the given member.",
        args=[['member', 'The member to ban.', 'required'], ['time', 'The time to ban the member for.', 'optional'], ['delete message days', 'The amount of messages to delete for the member. Defaults to 1.', 'optional'], ['reason', 'The reason for banning this member', 'optional']]        
    )
    @discord.app_commands.guilds(900465934257520671)
    @commands.check(isGloballyEnabled)
    @discord.app_commands.check(isGloballyEnabled)
    @commands.check(isEnabled)
    @discord.app_commands.check(isEnabled)
    @commands.check(checkForPerms)
    @discord.app_commands.check(checkForPerms)
    @discord.app_commands.rename(deleteMessageDays="delete_message_days")
    @discord.app_commands.describe(member="The member to ban.")
    @discord.app_commands.describe(time="The time to ban the member for. (optional)")
    @discord.app_commands.describe(deleteMessageDays="The amount of messages to delete for the member. Default 1 (optional)")
    @discord.app_commands.describe(reason="The reason for banning this member. (optional)")
    async def _ban(
        self,
        ctx: Union[commands.Context, discord.Interaction],
        member: Optional[discord.Member],
        time: Optional[str],
        deleteMessageDays: Optional[str],
        *,
        reason: Optional[str]
    ):
        with open("data.json") as f:
            data: dict = json.load(f)
        
        guildData = data[str(ctx.guild.id)]
        if member is None:
            response = returnEmbedOrMessage(ctx)
            await ctx.send(embed=response)
            return
            
        
async def setup(bot: Bot) -> None:
    await bot.add_cog(
        banCommand(
            bot=bot
        )
    )