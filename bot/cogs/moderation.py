import datetime
import json
import os
import time
import discord
from discord.ext import commands

from typing import Union, Optional

def formatString(string: str):
    #to do
    return string

def logToDb(ctx: Union[discord.Interaction, commands.Context], member: discord.Member, type: str, reason: str):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    author = ctx.author or ctx.user
    guildData: dict = data[str(ctx.guild.id)]
    if not str(member.id) in guildData['moderation']['modLogs']:
        guildData['moderation']['modLogs'][str(member.id)] = []
    guildData['moderation']['modLogs'][str(member.id)].append(
        {
            "member": member.id,
            "moderator": author.id,
            "type": type,
            "time": time.time(),
            "reason": reason
        }
    )
    with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)

def checkForPerms(ctx: Union[discord.Interaction, commands.Context]):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    author = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    for role in author.roles:
        if role.id in data[str(ctx.guild.id)]['moderation']['moderatorRoles']:
            return True
        elif role.id in data[str(ctx.guild.id)]['moderation']['administratorRoles']:
            return True
    if author.guild_permissions.ban_members or author.guild_permissions.administrator: 
        return True

def allowed(ctx: Union[discord.Interaction, commands.Context], commandName: str):
    with open("data.json", mode='r') as f:
        data = json.load(f)
    return data[str(ctx.guild.id)]['moderation']['commands'][commandName]['enabled']

def returnLogsChannel(bot: commands.Bot, guildId: int):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    return bot.get_channel(data[str(guildId)]['moderation']['logsChannel'])

def globalAllowed(ctx: Union[discord.Interaction, commands.Context]):
    with open("globalStuff.json", mode="r") as f:
        data: dict = json.load(f)
    return data[ctx.command.name]

class moderationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info(f"cogs.Moderation is now ready!")

    @commands.hybrid_command(
        name="ban",
        description="Bans the given member.",
        usage="<member> [delete message] [reason]",
        cooldownLimit=[5, "seconds"]
    )
    @discord.app_commands.check(globalAllowed)
    @discord.app_commands.check(checkForPerms)
    @commands.check(globalAllowed)
    @commands.check(checkForPerms)
    @discord.app_commands.guilds(900465934257520671)
    async def _ban(self, ctx: commands.Context, member: Optional[discord.Member], delete_messages: Optional[str], *, reason: Optional[str]):
        if not delete_messages: delete_messages = ""
        if not reason: reason = ""
        author = ctx.author or ctx.user
        if author.bot: return
        enabled = allowed(ctx, "ban")
        with open("data.json", mode="r") as f:
            data: dict = json.load(f)
        if not enabled: return await ctx.send(data[str(ctx.guild.id)]['disabledCommandMessage'])
        if member is None:
            embed = discord.Embed(
                color=discord.Color.from_str(os.getenv('DEFAULTEMBEDCOLOR')),
                title="Ban Command",
                description=f"**Description:** Bans the given member.\n**Cooldown:** 5 seconds\n**Usage:** {ctx.prefix}ban <member> [delete messages] [reason]\n**Example:**\n{ctx.prefix}ban @DeadSafari 7 Breaking Rule 34.\n{ctx.prefix}ban 958390293760184392 Breaking rule 4.\n{ctx.prefix}ban DeadSafari",
                timestamp=datetime.datetime.now()
            )
            await ctx.send(embed=embed)
            return
        try: 
            delete_messagesInt = int(delete_messages)
            if delete_messagesInt > 7: return await ctx.send(":x: `delete messages` argument cannot exceed 7 days!")
        except:
            delete_messagesInt = 0
            reason = delete_messages + " " + reason
            if not reason: reason = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDefaultReason']
        if not ctx.guild.me.guild_permissions.ban_members:
            return await ctx.send(":x: I don't have the `ban members` permission!")
        if member == author:
            return await ctx.send(":x: You can't ban yourself!")
        if member == ctx.guild.owner:
            return await ctx.send(":x: You can't ban the server owner!")
        if not ctx.guild.me.top_role > member.top_role:
            return await ctx.send(":x: I can't ban this member, because I don't have a role higher than them.")
        if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banMessageType'] == "embed":
            ctxBed = discord.Embed()
            ctxBed.title = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banEmbedTitle']
            ctxBed.description = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banEmbedDescription']
            if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banIncludeTimestamp']:
                ctxBed.timestamp = datetime.datetime.now()
            ctxBed.color = discord.Color.from_str(data[str(ctx.guild.id)]['moderation']['commands']['ban']['banEmbedColor'])
        else:
            message = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banMessage']
        if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDm']:
            if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageType'] == "embed":
                banDm = discord.Embed()
                banDm.title = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageEmbedTitle']
                banDm.description = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageEmbedDescription']
                banDm.color = discord.Color.from_str(data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageEmbedColor'])
                if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageEmbedIncludeTimestamp']:
                    banDm.timestamp = datetime.datetime.now()
            else:
                dmMessage = data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessage']
        logsEmbed = discord.Embed(
            description=f"**Banned by:** {author} | {author.id}\n**Member Banned:** {member} {member.id}\n**Reason:** {reason}",
            color=discord.Color.from_str(os.getenv("DEFAULTEMBEDCOLOR")),
            timestamp=datetime.datetime.now()
        )
        logsEmbed.set_author(name="Member Banned")
        if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banMessageType'] == "embed":
            await ctx.send(embed=ctxBed)
        else:
            await ctx.send(message)
        if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDm']:
            if data[str(ctx.guild.id)]['moderation']['commands']['ban']['banDmMessageType'] == "embed":
                try: await member.send(embed=banDm)
                except: pass
            else:
                try:
                    await member.send(dmMessage)
                except: pass
        # await member.ban(reason=reason, delete_message_days=delete_messagesInt)
        logToDb(
            ctx=ctx,
            member=member,
            type="ban",
            reason=reason
        )
        LogsChannel = returnLogsChannel(self.bot, ctx.guild.id)
        if LogsChannel:
            await LogsChannel.send(embed=logsEmbed)
    @commands.hybrid_command(
        name="kick",
        description="Kicks the given member.",
        usage="<member> [reason]",
        cooldownLimit=[5, "seconds"]
    )
    @discord.app_commands.check(globalAllowed)
    @discord.app_commands.check(checkForPerms)
    @commands.check(globalAllowed)
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
        enabled = allowed(ctx, "kick")
        with open("data.json", mode="r") as f:
            data: dict = json.load(f)
        if not enabled: return await ctx.send(data[str(ctx.guild.id)]['disabledCommandMessage'])
        if member is None:
            embed = discord.Embed(
                color=discord.Color.from_str(os.getenv('DEFAULTEMBEDCOLOR')),
                title="Kick Command",
                description=f"**Description:** Kicks the given member.\n**Cooldown:** 5 seconds\n**Usage:** {ctx.prefix}ban <member> [reason]\n**Example:**\n{ctx.prefix}kick @DeadSafari Breaking Rule 34.\n{ctx.prefix}ban 958390293760184392 Breaking rule 4.\n{ctx.prefix}ban DeadSafari",
                timestamp=datetime.datetime.now()
            )
            await ctx.send(embed=embed)
            return


async def setup(bot):
    await bot.add_cog(moderationCommands(bot=bot))