import json
import discord
from discord.ext import commands
from typing import Union

def returnEmbedOrMessage(ctx: Union[discord.Interaction, commands.Context]):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    guildData = data[str(ctx.guild.id)]
    messageData = guildData['moderation']['commands'][ctx.command.name]
    if messageData[ctx.command.name+"MessageType"] == "embed":
        embedData = messageData[ctx.command.name+"Embed"]
        if embedData['url'] != "null":
            embed  = discord.Embed(url=embedData['url'])
        else:
            embed = discord.Embed()
        if embedData['title'] != "null":
            print('title thing')
            embed.title = embedData['title']
        if embedData['description'] != "null":
            print('description thing')
            embed.description = embedData['description']
        if embedData['color'] != "null":
            print('color thing')
            embed.color = discord.Color.from_str(embedData['color'])
        if embedData['timestamp']:
            print('timestamp thing')
            embed.timestamp = ctx.message.created_at
        for field in embedData['fields']:
            print('field thing')
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field['inline']
            )
        if embedData['thumbnail_url'] != "null":
            print('thumbnail url thing')
            embed.set_thumbnail(url=embedData['thumbnail_url'])
        if embedData['image_url'] != "null":
            print('image url thing')
            embed.set_image(url=embedData['image_url'])
        embed.set_author(
            name=None if embedData['author']['name'] == "null" else embedData['author']['name'],
            icon_url=None if embedData['author']['icon_url'] == "null" else embedData['author']['icon_url'],
            url = None if embedData['author']['url'] == "null" else embedData['author']['url']
        )
        embed.set_footer(
            text="" if embedData['footer']['text'] == "null" else embedData['footer']['text'],
            icon_url=None if embedData['footer']['icon_url'] == "null" else embedData['footer']['icon_url'],
        )
        return embed
