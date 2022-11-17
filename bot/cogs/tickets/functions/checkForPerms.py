import json
import discord
from discord.ext import commands
from typing import Union

def checkForPerms(ctx: Union[discord.Interaction, commands.Context]):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    author = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    return author.guild_permissions.administrator