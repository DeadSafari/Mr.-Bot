import json
import discord
from discord.ext import commands
from typing import Union
import time
from uuid import uuid4

def logToDb(ctx: Union[discord.Interaction, commands.Context], member: discord.Member, type: str, reason: str, argTime: str = "0"):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    author = ctx.user
    guildData: dict = data[str(ctx.guild.id)]
    guildData['moderation']['modLogs'].append(
        {
            uuid4():
            { 
            "member": member.id,
            "moderator": author.id,
            "type": type,
            "timestamp": time.time(),
            "time": argTime,
            "reason": reason
            }
        }
    )
    with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)