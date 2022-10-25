import json
import discord
from discord.ext import commands
from typing import Union

def isEnabled(ctx: Union[discord.Interaction, commands.Context], commandName: str):
    with open("data.json", mode='r') as f:
        data = json.load(f)
    return data[str(ctx.guild.id)]['moderation']['commands'][commandName]['enabled']