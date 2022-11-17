import json
import discord
from discord.ext import commands
from typing import Union
from bot.functions.formatString import formatString
import datetime

def returnEmbedOrMessage(ctx: Union[discord.Interaction, commands.Context], reason: str, member, embedData):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    guildData = data[str(ctx.guild.id)]
    messageData = guildData['moderation']['commands'][ctx.command.name]
    if embedData['url'] != "null":
        embed  = discord.Embed(embedData['url'])
    else:
        embed = discord.Embed()
    if embedData['title'] != "null":
        embed.title = formatString(embedData['title'], ctx=ctx, reason=reason, member=member)
    if embedData['description'] != "null":
        embed.description = formatString(embedData['description'], ctx=ctx, reason=reason, member=member)
    if embedData['color'] != "null":
        embed.color = discord.Color.from_str(embedData['color'])
    if embedData['timestamp']:
        embed.timestamp = datetime.datetime.now()
    for field in embedData['fields']:
        embed.add_field(
            name=formatString(field['name'], ctx=ctx, reason=reason, member=member),
            value=formatString(field['value'], ctx=ctx, reason=reason, member=member),
            inline=field['inline']
        )
    if embedData['thumbnail_url'] != "null":
        embed.set_thumbnail(url=embedData['thumbnail_url'])
    if embedData['image_url'] != "null":
        embed.set_image(url=embedData['image_url'])
    embed.set_author(
        name="" if embedData['author']['name'] == "null" else formatString(embedData['author']['name'], ctx=ctx, reason=reason, member=member),
        icon_url=None if embedData['author']['icon_url'] == "null" else embedData['author']['icon_url'],
        url = None if embedData['author']['url'] == "null" else embedData['author']['url']
    )
    embed.set_footer(
        text=None if embedData['footer']['text'] == "null" else formatString(embedData['footer']['text'], ctx=ctx, reason=reason, member=member),
        icon_url=None if embedData['footer']['icon_url'] == "null" else embedData['footer']['icon_url'],
    )
    return embed