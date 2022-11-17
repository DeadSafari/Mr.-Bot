import discord
from discord.ext import commands
from typing import Union
from bot.functions.formatString import formatString
from bot.functions.isProtected import isProtected

def checksForCommands(ctx: Union[commands.Context, discord.Interaction], member: discord.Member, author: discord.Member, commandData: dict, reason: str):
    if not ctx.guild.me.guild_permissions.ban_members:
        return(formatString(
            commandData['errors'][f'failed{ctx.command.name.capitalize()}PermissionCheck'],
            ctx=ctx,
            reason=reason,
            member=member
        ))
    if author == member:
        return formatString(
            commandData['errors']['authorEqualsMember'],
            ctx=ctx,
            reason=reason,
            member=member
        )
        
    if member == ctx.guild.owner:
        return formatString(
            commandData['errors']['ownerEqualsMember'],
            ctx=ctx,
            reason=reason,
            member=member
        )
    if isProtected(ctx=ctx, member=member):
        return formatString(
            commandData['errors']['protectedRole'],
            ctx=ctx,
            member=member,
            reason=reason
        )
    if not author.top_role > member.top_role:
        return formatString(
            commandData['errors']['roleHierarchyError'],
            ctx=ctx,
            member=member,
            reason=reason
        )