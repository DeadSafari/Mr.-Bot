import asyncio
import traceback
import discord
from discord.ext import commands
import logging
from discord.utils import setup_logging
from dotenv import load_dotenv
import os
import json

class hybridCommand(commands.Command):
    def __init__(self):
        super().__init__()

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log = logging.getLogger("Mr. Bot")

        self.TOKEN: str = os.getenv("TOKEN")
        self.trueReady: bool = False

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=900465934257520671))

    async def on_ready(self):
        self.log.info("Logged in.")
        self.log.info("Checking & fixing the database...")
        updateDatabase(self)
        self.trueReady = True
        self.log.info("Finished checking & fixing the database.")
        self.log.info("===========================================")
        self.log.info(f"Bot Name: {self.user}")
        self.log.info(f"Bot ID: {self.user.id}")
        self.log.info(f"Users: {len(self.users)}")
        self.log.info(f"Guilds: {len(self.guilds)}")
        self.log.info("===========================================")

    async def on_error(self, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if not isinstance(error, commands.errors.CommandNotFound):
            traceback.print_exc()
        return

def getPrefix(bot: Bot, message: discord.Message):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    return data[str(message.guild.id)]['prefix']

def getStripAfterPrefix(bot: Bot, message: discord.Message):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    return data[str(message.guild.id)]['stripAfterPrefix']

async def main():
    load_dotenv()
    intents = discord.Intents.all()
    intents.presences = False
    bot = Bot(
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
                await bot.load_extension(f"cogs.{cog[:-3]}")
            except:
                traceback.print_exc()
    await bot.start(os.getenv('TOKEN'))

def addGuildsToDatabase(guildIds: list, data: dict):
    for id in guildIds:
        data[int(id)] = {"prefix": "?", "stripAfterPrefix": False}
    return data

def updateDatabase(bot: Bot):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    with open("updates.json", mode="r") as f:
        exp: dict = json.load(f)
    keys = exp.keys()
    for key in data:
        for updatedKey in keys:
            data[key][updatedKey] = exp[updatedKey]
    unAddedGuilds = []
    for guild in bot.guilds:
        if not str(guild.id) in data:
            unAddedGuilds.append(guild.id)
    data = addGuildsToDatabase(unAddedGuilds, data=data)
    exp.clear()
    with open("updates.json", mode="w") as f:
        json.dump(exp, f, indent=4)
    with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)
    return

asyncio.run(main())