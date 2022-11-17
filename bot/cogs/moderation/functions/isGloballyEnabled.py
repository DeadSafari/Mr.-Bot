import json
import discord
from discord.ext import commands
from typing import Union

def isGloballyEnabled(ctx: Union[discord.Interaction, commands.Context]):
    with open("globalStuff.json", mode="r") as f:
        data: dict = json.load(f)
    return data[ctx.command.name]