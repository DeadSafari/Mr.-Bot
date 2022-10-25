import json
import discord
from discord.ext import commands
from typing import Union

def returnLogsChannel(bot: commands.Bot, guildId: int):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    return bot.get_channel(data[str(guildId)]['moderation']['logsChannel'])