import json
import discord
from discord.ext import commands
from typing import Union
import time

def logToDb(ctx: Union[discord.Interaction, commands.Context], member: discord.Member, type: str, reason: str):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    author = ctx.author or ctx.user
    guildData: dict = data[str(ctx.guild.id)]
    if not str(member.id) in guildData['moderation']['modLogs']:
        guildData['moderation']['modLogs'][str(member.id)] = []
    guildData['moderation']['modLogs'][str(member.id)].append(
        {
            "member": member.id,
            "moderator": author.id,
            "type": type,
            "time": time.time(),
            "reason": reason
        }
    )
    with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)