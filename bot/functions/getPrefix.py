from bot.bot import Bot
import discord
import json

def getPrefix(bot: Bot, message: discord.Message):
    with open("data.json", mode="r") as f:
        data = json.load(f)
    return data[str(message.guild.id)]['prefix']