from discord.ext.commands import Bot
import discord
import json

def getStripAfterPrefix(bot: Bot, message: discord.Message):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    return data[str(message.guild.id)]['stripAfterPrefix']