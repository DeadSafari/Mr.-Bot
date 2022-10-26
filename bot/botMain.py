#imports
import traceback
import discord
from discord.ext import commands
import logging
from discord.utils import setup_logging
from dotenv import load_dotenv
import os
import json
from bot.functions.updateDb import updateDb
from bot.functions.getPrefix import getPrefix
from bot.functions.getStripAfterPrefix import getStripAfterPrefix

class Bot(commands.Bot):
    def __init__(
        self,
        **kwargs) -> None:
        super().__init__(
            **kwargs
        )

        #setup an instance of the logging.getLogger
        self.log: logging.getLogger = logging.getLogger("Mr. Bot")

        self.TOKEN: str = os.getenv("TOKEN")

    async def setup_hook(self) -> None:
        await self.tree.sync(
            guild=discord.Object(
                id=900465934257520671
            )
        )

    async def on_ready(self):
        self.log.info("Logged in.")
        self.log.info("Checking & fixing the database...")
        updateDb(
            bot=self
        )
        self.log.info("Finished checking & fixing the database.")
        self.log.info("===========================================")
        self.log.info(f"Bot Name: {self.user}")
        self.log.info(f"Bot ID: {self.user.id}")
        self.log.info(f"Users: {len(self.users)}")
        self.log.info(f"Guilds: {len(self.guilds)}")
        self.log.info("===========================================")

    async def on_error(self, error: Exception) -> None:
        traceback.print_exc()

    async def on_command_error(self, context: commands.Context, error: Exception) -> None:
        if isinstance(
            error,
            commands.CommandNotFound
        ):
            return

async def main():
    #load the .env file
    load_dotenv()
    intents = discord.Intents.all()
    intents.presences = False
    bot: Bot = Bot(
        command_prefix=getPrefix,
        intents=intents,
        case_insensitive=True,
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name="https://mr-bot.ml/"),
        strip_after_prefix=getStripAfterPrefix,
        help_command=None
    )
    setup_logging()
    for cog in os.listdir("./bot/cogs"):
        if cog.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{cog[:-3]}")
            except:
                traceback.print_exc()
    await bot.start(os.getenv('TOKEN'))