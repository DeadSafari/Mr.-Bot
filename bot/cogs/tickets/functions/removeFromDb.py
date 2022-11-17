import json
import discord
from discord.ext import commands
from typing import Union
import time

def removeFromDb(ctx: Union[discord.Interaction, commands.Context], uuid: str):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    author = ctx.user
    guildData: dict = data[str(ctx.guild.id)]
    for modlog in guildData['moderation']['modLogs']:
        if uuid in modlog:
            guildData['moderation']['modLogs'].remove(modlog)
            with open("data.json", mode="w") as f:
                json.dump(data, f, indent=4)
            return True

    return False
