#imports
import asyncio
import traceback
import discord
from discord.ext import commands
import logging
from discord.utils import setup_logging
from dotenv import load_dotenv
import os
import time

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

    async def on_command_error(self, ctx, error):
        print("we got a command error")

    async def on_ready(self):
        self.startTime = time.time()
        self.log.info("Logged in.")
        self.log.info("Checking & fixing the database...")
        self.log.info("Finished checking & fixing the database.")
        self.log.info("===========================================")
        self.log.info(f"Bot Name: {self.user}")
        self.log.info(f"Bot ID: {self.user.id}")
        self.log.info(f"Users: {len(self.users)}")
        self.log.info(f"Guilds: {len(self.guilds)}")
        self.log.info("===========================================")
        self.loop = asyncio.get_running_loop()

intents = discord.Intents.all()
intents.presences = False
bot: Bot = Bot(
    command_prefix="mr.",
    intents=intents,
    case_insensitive=True,
    status=discord.Status.online,
    activity=discord.Activity(type=discord.ActivityType.watching, name="https://www.mr-bot.ml/"),
    strip_after_prefix=True,
    help_command=None
)

def return_bot():
    return bot

async def main():
    #load the .env file
    load_dotenv()
    setup_logging()
    bot.return_bot = return_bot
    for cog in os.listdir("./bot/cogs"):
        if cog != "__pycache__":
            for file in os.listdir("./bot/cogs/"+cog):
                if file.endswith(".py"):
                    try:
                        await bot.load_extension("bot.cogs."+cog+"."+file[:-3])
                    except Exception as e:
                        traceback.print_exc()
    await bot.start(os.getenv('TOKEN'))
