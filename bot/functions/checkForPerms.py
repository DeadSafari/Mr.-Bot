import json
import discord
from discord.ext import commands
from typing import Union

def checkForPerms(ctx: Union[discord.Interaction, commands.Context]):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    author = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    for role in author.roles:
        if role.id in data[str(ctx.guild.id)]['moderation']['moderatorRoles']:
            return True
        elif role.id in data[str(ctx.guild.id)]['moderation']['administratorRoles']:
            return True
    if author.guild_permissions.ban_members or author.guild_permissions.administrator: 
        return True