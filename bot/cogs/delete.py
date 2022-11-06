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
from bot.functions.returnEmbedOrMessage import returnEmbedOrMessage
from bot.functions.removeFromDb import removeFromDb

class deleteCommand(commands.Cog):
    def __init__(
        self,
        bot: Bot
    ):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("commands.Delete is now ready!")
        with open('tasks.json', 'r') as f:
            tasks: dict = json.load(f)
    
    @discord.app_commands.command(
        name="delete",
        description="Deletes the given modlog.",
        # args=[['member', 'The member to ban.', 'required'], ['time', 'The time to ban the member for.', 'optional'], ['delete message days', 'The amount of messages to delete for the member. Defaults to 1.', 'optional'], ['reason', 'The reason for banning this member', 'optional']]
    )
    @discord.app_commands.describe(id="The ID of the modlog to delete.")
    @discord.app_commands.guilds(900465934257520671)
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(isEnabled)
    @discord.app_commands.check(checkForPerms)
    async def _delete(
        self,
        interaction: discord.Interaction,
        id: str = None
    ):
        await interaction.response.defer()
        with open("data.json") as f:
            data: dict = json.load(f)
        guildData = data[str(interaction.guild.id)]
        commandData = guildData['moderation']['commands'][interaction.command.name]
        if id is None:
            if commandData[interaction.command.name+'MessageType'] == "embed":
                response = returnEmbedOrMessage(
                    ctx=interaction,
                    reason="",
                    member=self.bot.user,
                    embedData=commandData[interaction.command.name+'Embed']
                )
                await interaction.followup.send(embed=response)
                return

        response = removeFromDb(
            ctx=interaction,
            uuid=id
        )
        
        if not response:
            error = formatString(
                commandData['erros']['idNotFound']
            )
            await interaction.followup.send(content=error)
            return

        if commandData[interaction.command.name+"SendType"] == "embed":
            response = returnEmbedOrMessage(interaction, reason="", member=self.bot.user, embedData=commandData[interaction.command.name+'SendEmbed'])
    
        else:
            response = formatString(
                commandData[interaction.command.name+'Message'],
                ctx=interaction,
                member=self.bot.user,
                reason=""
            )

        if isinstance(response, discord.Embed):
            await interaction.followup.send(embed=response)
        else:
            await interaction.followup.send(content=response)


async def setup(bot: Bot) -> None:
    await bot.add_cog(
        deleteCommand(
            bot=bot
        )
    )