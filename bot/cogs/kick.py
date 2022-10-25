import datetime
import json
import os
import time
import discord
from discord.ext import commands
from typing import Union, Optional
from bot.functions.checkForPerms import checkForPerms
from bot.functions.formatString import formatString, formatString
from bot.functions.isEnabled import isEnabled
from bot.functions.isGloballyEnabled import isGloballyEnabled
from bot.functions.logToDb import logToDb
from bot.functions.returnLogsChannel import returnLogsChannel

class kickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f"commands.Kick is now ready!")

    @commands.hybrid_command(
        name="kick",
        description="Kicks the given member.",
        usage="<member> [reason]",
        cooldownLimit=[5, "seconds"]
    )
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(checkForPerms)
    @commands.check(isGloballyEnabled)
    @commands.check(checkForPerms)
    @discord.app_commands.guilds(900465934257520671)
    async def _kick(
        self,
        ctx: Union[discord.Interaction, commands.Context],
        member: Optional[discord.Member],
        *,
        reason: Optional[str]
    ):
        if not reason: reason = ""
        author = ctx.author or ctx.user
        if author.bot: return
        enabled = isEnabled(ctx, "kick")
        with open("data.json", mode="r") as f:
            data: dict = json.load(f)
        if not enabled: return await ctx.send(data[str(ctx.guild.id)]['disabledCommandMessage'])
        if member is None:
            embed = discord.Embed(
                color=discord.Color.from_str(os.getenv('DEFAULTEMBEDCOLOR')),
                title="Kick Command",
                description=f"**Description:** Kicks the given member.\n**Cooldown:** 5 seconds\n**Usage:** {ctx.prefix}kick <member> [reason]\n**Example:**\n{ctx.prefix}kick @DeadSafari Breaking Rule 34.\n{ctx.prefix}kick 958390293760184392 Breaking rule 4.\n{ctx.prefix}kick DeadSafari",
                timestamp=datetime.datetime.now()
            )
            await ctx.send(embed=embed)
            return
        if not ctx.guild.me.guild_permissions.kick_members:
            return await ctx.send(":x: I don't have the `kick members` permission!")
        if member == author:
            return await ctx.send(":x: You can't kick yourself!")
        if member == ctx.guild.owner:
            return await ctx.send(":x: You can't kick the server owner!")
        if not ctx.guild.me.top_role > member.top_role:
            return await ctx.send(":x: I can't kick this member, because I don't have a role higher than them.")
        if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickMessageType'] == "embed":
            ctxBed = discord.Embed()
            ctxBed.title = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickEmbedTitle']
            ctxBed.description = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickEmbedDescription']
            if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickIncludeTimestamp']:
                ctxBed.timestamp = datetime.datetime.now()
            ctxBed.color = discord.Color.from_str(data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickEmbedColor'])
        else:
            message = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickMessage']
        if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDm']:
            if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageType'] == "embed":
                banDm = discord.Embed()
                banDm.title = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageEmbedTitle']
                banDm.description = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageEmbedDescription']
                banDm.color = discord.Color.from_str(data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageEmbedColor'])
                if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageEmbedIncludeTimestamp']:
                    banDm.timestamp = datetime.datetime.now()
            else:
                dmMessage = data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessage']
        logsEmbed = discord.Embed(
            description=f"**Kicked by:** {author} | {author.id}\n**Member Kicked:** {member} {member.id}\n**Reason:** {reason}",
            color=discord.Color.from_str(os.getenv("DEFAULTEMBEDCOLOR")),
            timestamp=datetime.datetime.now()
        )
        logsEmbed.set_author(name="Member Kicked")
        if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickMessageType'] == "embed":
            await ctx.send(embed=ctxBed)
        else:
            await ctx.send(message)
        if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDm']:
            if data[str(ctx.guild.id)]['moderation']['commands']['kick']['kickDmMessageType'] == "embed":
                try: await member.send(embed=banDm)
                except: pass
            else:
                try:
                    await member.send(dmMessage)
                except: pass
        await member.kick(reason=reason)
        logToDb(
            ctx=ctx,
            member=member,
            type="kick",
            reason=reason
        )
        LogsChannel = returnLogsChannel(self.bot, ctx.guild.id)
        if LogsChannel:
            await LogsChannel.send(embed=logsEmbed)


async def setup(bot):
    await bot.add_cog(kickCommand(bot=bot))