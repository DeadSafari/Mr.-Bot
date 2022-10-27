import json
import discord
from discord.ext import commands
from typing import Union

def isProtected(ctx: Union[discord.Interaction, commands.Context], member: discord.Member):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    guildData = data[str(ctx.guild.id)]
    for role in member.roles:
        if role.id in guildData['protectedRoles']:
            return True
    return False
