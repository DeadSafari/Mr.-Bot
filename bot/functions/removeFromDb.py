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
    for i in guildData['moderation']['modLogs']:
        if uuid in i:
            guildData['moderation']['modLogs'].remove(i)
            with open("data.json", mode="w") as f:
                json.dump(data, f, indent=4)
            return True
        else:
            return False
