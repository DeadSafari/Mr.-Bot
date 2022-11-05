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

class muteCommand(commands.Cog):
    def __init__(
        self,
        bot: Bot
    ):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("commands.Mute is now ready!")
        with open('tasks.json', 'r') as f:
            tasks: dict = json.load(f)
        for task in tasks['mutes']:
            member = self.bot.get_user(task['member'])
            if member is None: 
                member = await self.bot.fetch_user(task['member'])
                if member is None: continue
            guild = self.bot.get_guild(task['guild'])
            if guild is None: continue
            role = guild.get_role(task['role_id'])
            self.bot.loop.call_later(task['timestamp'], asyncio.create_task(member.remove_roles(role)))

    
    @discord.app_commands.command(
        name="mute",
        description="Mutes the given member.",
        # args=[['member', 'The member to ban.', 'required'], ['time', 'The time to ban the member for.', 'optional'], ['delete message days', 'The amount of messages to delete for the member. Defaults to 1.', 'optional'], ['reason', 'The reason for banning this member', 'optional']]
    )
    @discord.app_commands.describe(member="The member to mute.")
    @discord.app_commands.describe(time="The time to mute the member for. (optional)")
    @discord.app_commands.describe(reason="The reason for muting this member. (optional)")
    @discord.app_commands.guilds(900465934257520671)
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(isEnabled)
    @discord.app_commands.check(checkForPerms)
    async def _ban(
        self,
        interaction: discord.Interaction,
        member: Union[discord.Member, discord.User] = None,
        time: Optional[str] = None,
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

        muteRole = interaction.guild.get_role(guildData['moderation']['muteRoleId'])
        if muteRole is None:
            await interaction.followup.send(content=formatString(commandData['errors']['muteRoleNotFound'],
                ctx=interaction,
                member=member,
                reason=formatString(reason, ctx=interaction, member=member, reason=reason)))
            return

        try:
            await member.add_roles(muteRole, reason=formatString(reason, ctx=interaction, member=member, reason=reason))
        except Exception as e:
            await interaction.followup.send(content="Hey this is rare. For some reason, I was unable to add the mute role to this member. You might wanna try again. This error has already been logged, and we're working on fixing it! Sorry for the inconvenience!")

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
                title="Member Muted",
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

        self.bot.loop.call_later(seconds, asyncio.create_task(member.remove_roles(muteRole)))
        
        with open("tasks.json", mode="r") as f:
            data: dict = json.load(f)
        
        timestamp_unmute = datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))

        data['mute'].append(
            {"type": "mute", "member": member.id, "guild": interaction.guild.id, "timestamp": timestamp_unmute, "role_id": guildData['moderation']['muteRoleId']}
        )
        with open("tasks.json", mode="w") as f:
            json.dump(data, f, indent=4)

        logToDb(
            interaction,
            member=member,
            type="mute",
            reason=reason,
            argTime=time
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(
        muteCommand(
            bot=bot
        )
    )