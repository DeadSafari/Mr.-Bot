#imports
import datetime
import json
import os
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from typing import List, Tuple, Union, Optional
from bot.functions.checkForPerms import checkForPerms
from bot.functions.formatString import formatString 
from bot.functions.isEnabled import isEnabled
from bot.functions.isGloballyEnabled import isGloballyEnabled
from bot.functions.logToDb import logToDb
from bot.functions.returnLogsChannel import returnLogsChannel
from bot.functions.returnEmbedOrMessage import returnEmbedOrMessage
from bot.functions.isProtected import isProtected
from bot.functions.checksForCommands import checksForCommands

class banCommand(commands.Cog):
    def __init__(
        self,
        bot: Bot
    ):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("commands.Ban is now ready!")
    
    @discord.app_commands.command(
        name="ban",
        description="Bans the given member(s).",
        # args=[['member', 'The member to ban.', 'required'], ['time', 'The time to ban the member for.', 'optional'], ['delete message days', 'The amount of messages to delete for the member. Defaults to 1.', 'optional'], ['reason', 'The reason for banning this member', 'optional']]
    )
    @discord.app_commands.describe(member="The member to ban.")
    @discord.app_commands.describe(time="The time to ban the member for. (optional)")
    @discord.app_commands.describe(delete_message_days="The amount of messages to delete for the member. Default 1 (optional)")
    @discord.app_commands.describe(reason="The reason for banning this member. (optional)")
    @discord.app_commands.guilds(900465934257520671)
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(isEnabled)
    @discord.app_commands.check(checkForPerms)
    async def _ban(
        self,
        interaction: discord.Interaction,
        member: Union[discord.Member, discord.User] = None,
        time: Optional[str] = None,
        delete_message_days: Optional[int] = 0,
        reason: Optional[str] = None
    ):
        await interaction.response.defer()
        with open("data.json") as f:
            data: dict = json.load(f)
        guildData = data[str(interaction.guild.id)]
        sendType = guildData['moderation']['commands'][interaction.command.name]
        commandData = guildData['moderation']['commands'][interaction.command.name]
        if member is None:
            response = returnEmbedOrMessage(interaction)
            await interaction.followup.send(embed=response)
            return

        errorMessage = checksForCommands(
            ctx=interaction,
            member=member,
            author=interaction.user,
            reason=reason,
            commandData=commandData
        )
        if errorMessage:
            return await interaction.followup.send(content=errorMessage)
        self.bot.log.info("converting time")
        try:
            seconds = time[:-1] #Gets the numbers from the time argument, start to -1
            duration = time[-1] #Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await interaction.followup.send(content="Invalid duration input")
                return
            self.bot.log.info("converted time")
        except Exception as e:
            self.bot.log.info("exception")
            traceback.print_exc()
            await interaction.followup.send(content="Invalid time input")
            return

        await interaction.followup.send(content="this is a message")

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        banCommand(
            bot=bot
        )
    )