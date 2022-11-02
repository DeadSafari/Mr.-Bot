#imports
import asyncio
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
        with open('tasks.json', 'r') as f:
            tasks: dict = json.load(f)
        for task in tasks['bans']:
            member = self.bot.get_user(task['member'])
            if member is None: 
                member = await self.bot.fetch_user(task['member'])
                if member is None: continue
            guild = self.bot.get_guild(task['guild'])
            if guild is None: continue
            self.bot.loop.call_later(task['timestamp'], asyncio.create_task(guild.unban(member)))

    
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
        commandData = guildData['moderation']['commands'][interaction.command.name]
        if member is None:
            if commandData[interaction.command.name+'MessageType'] == "embed":
                response = returnEmbedOrMessage(
                    ctx=interaction,
                    reason=reason,
                    member=member,
                    embedData=commandData[interaction.command.name+'Embed']
                )
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
        if time:
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
                    await interaction.followup.send(
                        content=formatString(
                            commandData['errors']['failedTimeConvert'],
                            ctx=interaction,
                            member=member,
                            reason=reason
                    ))
                    return
                self.bot.log.info("converted time")
            except Exception as e:
                    self.bot.log.info("exception")
                    traceback.print_exc()
                    await interaction.followup.send(
                        content=formatString(
                            commandData['errors']['failedTimeConvert'],
                            ctx=interaction,
                            member=member,
                            reason=reason
                    ))
                    return
        else:
           seconds = 0

        if not reason:
            reason = commandData[interaction.command.name+'DefaultReason']

        if commandData[interaction.command.name+"SendType"] == "embed":
            response = returnEmbedOrMessage(interaction, reason=reason, member=member, embedData=commandData[interaction.command.name+'SendEmbed'])
    
        else:
            response = formatString(
                commandData[interaction.command.name+'Message'],
                ctx=interaction,
                member=member,
                reason=reason
            )

        if commandData[interaction.command.name+'Dm']:
            if commandData[interaction.command.name+'DmMessageType'] == "embed":
                dmResponse = returnEmbedOrMessage(interaction, reason=reason, member=member, embedData=commandData[interaction.command.name+'DmEmbed'])
            else:
                dmResponse = formatString(
                    commandData[interaction.command.name+'DmEmbed'],
                    ctx=interaction,
                    member=member,
                    reason=reason
                )
            try:
                if isinstance(dmResponse, discord.Embed):
                    await member.send(embed=dmResponse)
                else:
                    await member.send(content=dmResponse)
            except Exception as e:
                error = commandData['errors']['failedToSendDmToMember']
                if error != "null":
                    await interaction.followup.send(content=
                        formatString(
                            error,
                            ctx=interaction,
                            member=member,
                            reason=reason
                        )
                    )

        try:
            await interaction.guild.ban(
                member,
                reason=formatString(reason, ctx=interaction, member=member, reason=reason),
                delete_message_days=delete_message_days
            )
        except Exception as e:
            await interaction.followup.send(content="Hey this is rare. For some reason, I was unable to ban this member. You might wanna try again. This error has already been logged, and we're working on fixing it! Sorry for the inconvenience!")

            """
            Add Error logging system here later
            """

            return



        if isinstance(response, discord.Embed):
            await interaction.followup.send(embed=response)
        else:
            await interaction.followup.send(content=response)

        if commandData[interaction.command.name+"Logs"]:
            embed = discord.Embed(
                color=discord.Color.from_str(os.getenv('DEFAULTEMBEDCOLOR')),
                title="Member Banned",
                description=f"I can't be arsed to make this a custom thing yet. So here's the default embed. Sorry!"
            )
            channel = returnLogsChannel(self.bot, interaction.guild.id)
            if channel:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    await interaction.followup.send(content="Hey this is rare. For some reason, I was unable to send the logs to the logs channel. You might wanna try again. This error has already been logged, and we're working on fixing it! Sorry for the inconvenience!")

                    """
                    Add Error logging system here later
                    """

        if seconds == 0: 
            return

        self.bot.loop.call_later(seconds, asyncio.create_task(member.unban()))
        
        with open("tasks.json", mode="r") as f:
            data: dict = json.load(f)
        
        timestamp_unban = datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))

        data['bans'].append(
            {"type": "ban", "member": member.id, "guild": interaction.guild.id, "timestamp": timestamp_unban}
        )
        with open("tasks.json", mode="w") as f:
            json.dump(data, f, indent=4)

        logToDb(
            interaction,
            member=member,
            type="ban",
            reason=reason,
            argTime=time
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(
        banCommand(
            bot=bot
        )
    )