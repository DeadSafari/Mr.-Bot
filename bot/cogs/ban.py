#imports
import datetime
import json
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from typing import List, Tuple, Union, Optional
from bot.functions.checkForPerms import checkForPerms
from bot.functions.formatString import formatString, formatString
from bot.functions.isEnabled import isEnabled
from bot.functions.isGloballyEnabled import isGloballyEnabled
from bot.functions.logToDb import logToDb
from bot.functions.returnLogsChannel import returnLogsChannel
from bot.functions.returnEmbedOrMessage import returnEmbedOrMessage
from bot.functions.isProtected import isProtected

class banFlags(commands.FlagConverter, case_insensitive=True):
    # member: Union[discord.Member, discord.User] = commands.flag(
    #     name="member",
    #     aliases=['users', 'user', 'members'],
    #     description="The member to ban.",
    #     default=None
    # )
    delete_message_days: int = commands.flag(
        name="delete_message_days",
        aliases=['deleteMessageDays', 'delmsgdays', 'delmsg', 'del'],
        description="The number of days worth of messages to delete from the user in the guild. The minimum & default is 0 and the maximum is 7.",
        default=0
    )
    reason: str = commands.flag(
        name="reason",
        description="The reason for banning.",
        default=""
    )
    time: str = commands.flag(
        name='time',
        description="The amount of time to ban for.",
        default=""
    )

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
    # @discord.app_commands.rename(deleteMessageDays="delete_message_days")
    @discord.app_commands.describe(members="The member(s) to ban.")
    # @discord.app_commands.describe(time="The time to ban the member for. (optional)")
    # @discord.app_commands.describe(deleteMessageDays="The amount of messages to delete for the member. Default 1 (optional)")
    # @discord.app_commands.describe(reason="The reason for banning this member. (optional)")
    async def _ban(
        self,
        ctx: Union[commands.Context, discord.Interaction],
        members: commands.Greedy[Union[discord.Member, discord.User]],
        *,
        args: banFlags
    ):
        print(args)
        with open("data.json") as f:
            data: dict = json.load(f)
        # member = args.member
        reason = args.reason
        time = args.time
        delete_message_days = args.delete_message_days
        guildData = data[str(ctx.guild.id)]
        sendType = guildData['moderation']['commands'][ctx.command.name]
        commandData = guildData['moderation']['commands'][ctx.command.name]
        for member in members:
            if member is None:
                response = returnEmbedOrMessage(ctx)
                await ctx.send(embed=response)
                return
            if not ctx.guild.me.guild_permissions.ban_members:
                await ctx.send(formatString(
                    commandData['errors']['failedBanPermissionCheck'],
                    ctx=ctx,
                    reason=reason,
                    member=member
                ))
                return
            if ctx.author == member:
                await ctx.send(formatString(
                    commandData['errors']['authorEqualsMember'],
                    ctx=ctx,
                    reason=reason,
                    member=member
                ))
                return
            if member == ctx.guild.owner:
                await ctx.send(formatString(
                    commandData['errors']['ownerEqualsMember'],
                    ctx=ctx,
                    reason=reason,
                    member=member
                ))
                return
            if isProtected(ctx=ctx, member=member):
                await ctx.send(formatString(
                    commandData['errors']['protectedRole'],
                    ctx=ctx,
                    member=member,
                    reason=reason
                ))
                return
            if not ctx.author.top_role > member.top_role:
                await ctx.send(formatString(
                    commandData['errors']['roleHierarchyError'],
                    ctx=ctx,
                    member=member,
                    reason=reason
                ))
                return

        
            
        
async def setup(bot: Bot) -> None:
    await bot.add_cog(
        banCommand(
            bot=bot
        )
    )