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
from bot.cogs.moderation.functions.checkForPerms import checkForPerms
from bot.cogs.moderation.functions.formatString import formatString 
from bot.cogs.moderation.functions.isEnabled import isEnabled
from bot.cogs.moderation.functions.isGloballyEnabled import isGloballyEnabled
from bot.cogs.moderation.functions.logToDb import logToDb
from bot.cogs.moderation.functions.returnLogsChannel import returnLogsChannel
from bot.cogs.moderation.functions.returnEmbedOrMessage import returnEmbedOrMessage
from bot.cogs.moderation.functions.checksForCommands import checksForCommands

class kickCommand(commands.Cog):
    def __init__(
        self,
        bot: Bot
    ):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.moderation.Kick is now ready!")
        with open('tasks.json', 'r') as f:
            tasks: dict = json.load(f)
    
    @discord.app_commands.command(
        name="kick",
        description="Kicks the given member.",
        # args=[['member', 'The member to ban.', 'required'], ['time', 'The time to ban the member for.', 'optional'], ['delete message days', 'The amount of messages to delete for the member. Defaults to 1.', 'optional'], ['reason', 'The reason for banning this member', 'optional']]
    )
    @discord.app_commands.describe(member="The member to kick.")
    @discord.app_commands.describe(reason="The reason for kicking this member. (optional)")
    @discord.app_commands.guilds(900465934257520671)
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(isEnabled)
    @discord.app_commands.check(checkForPerms)
    async def _kick(
        self,
        interaction: discord.Interaction,
        member: Union[discord.Member, discord.User] = None,
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
            await interaction.guild.kick(
                member,
                reason=formatString(reason, ctx=interaction, member=member, reason=reason)
            )
        except Exception as e:
            await interaction.followup.send(content="Hey this is rare. For some reason, I was unable to kick this member. You might wanna try again. This error has already been logged, and we're working on fixing it! Sorry for the inconvenience!")

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
                title="Member Kicked",
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
        logToDb(
            interaction,
            member=member,
            type="kick",
            reason=reason,
            argTime="N/A"
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(
        kickCommand(
            bot=bot
        )
    )