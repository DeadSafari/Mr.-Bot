import discord
from discord.ext import commands
from bot.cogs.tickets.functions.checkForPerms import checkForPerms
from bot.cogs.tickets.functions.formatString import formatString 
from bot.cogs.tickets.functions.isEnabled import isEnabled
from bot.cogs.tickets.functions.isGloballyEnabled import isGloballyEnabled
from bot.cogs.tickets.functions.returnEmbedOrMessage import returnEmbedOrMessage
import json

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.tickets.Tickets is now ready!")

    @discord.app_commands.command(
        name="setup",
        description="Sets up the ticket system."
    )
    @discord.app_commands.guilds(900465934257520671)
    @discord.app_commands.check(isGloballyEnabled)
    @discord.app_commands.check(isEnabled)
    @discord.app_commands.check(checkForPerms)
    async def _setup(
        self,
        interaction: discord.Interaction
    ):
        with open("data.json", mode="r") as f:
            data = json.load(f)
        guildData = data[str(interaction.guild.id)]
        commandData = guildData['tickets']['commands'][interaction.command.name]
        response = returnEmbedOrMessage(
            ctx=interaction,
            reason="",
            member="",
            embedData=commandData[interaction.command.name+'Embed']
        )
        await interaction.response.send_message(embed=response)


async def setup(bot):
    await bot.add_cog(Ticket(bot))