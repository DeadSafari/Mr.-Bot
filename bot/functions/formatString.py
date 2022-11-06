import json
import discord
from discord.ext import commands
from typing import Optional, Union

def formatString(string: str, ctx: Union[commands.Context, discord.Interaction], member=None, reason: str=None):
    # with open("string.docs", mode="r") as f:
    #     data: dict = json.load(f)
    # astr: str
    if not member: member = ctx.user
    astr = string.replace("[member.fullName]", str(member)).replace("[member.id]", str(member.id)).replace("[member.name]", member.name).replace("[member.nickName]", member.display_name).replace("[member.tag]", str(member.discriminator)).replace("[member.avatar]", member.avatar.url if member.avatar else "Member has no avatar").replace("[member.nickAvatar]", member.display_avatar.url if member.display_avatar else "Member has no avatar").replace("[server.name]", ctx.guild.name).replace("[server.id]", str(ctx.guild.id)).replace("[server.owner]", str(ctx.guild.owner)).replace("[server.owner.id]", str(ctx.guild.owner_id)).replace("[prefix]", "/").replace("[reason]", str(reason))
    return astr
    # for attribute in data['attributes']:
    #     if attribute == "[member.fullName]":
    #         string = string.replace(attribute, str(member))
    #     if attribute == "[member.id]":
    #         string = string.replace(attribute, member.id)
    #     if attribute == "[member.name]":
    #         string = string.replace(attribute, member.name)
    #     if attribute == "[member.nickName]":
    #         string = string.replace(attribute, member.display_name)
    #     if attribute == "[member.tag]":
    #         string = string.replace(attribute, member.discriminator)
    #     if attribute == "[member.avatar]":
    #         string = string.replace(attribute, member.avatar.url)
    #     if attribute == "[member.nickAvatar]":
    #         string = string.replace(attribute, member.display_avatar.url)
    #     if attribute == "[member.banner]":
    #         string = string.replace(attribute, member.banner.url)
    #     if attribute == "[member.nickBanner]":
    #         string = string.replace(attribute, member.banner.url)
    #     if attribute == "[server.name]":
    #         string = string.replace(attribute, ctx.guild.name)
    #         print(string)
    #         print('got here')
    #     if attribute == "[server.id]":
    #         string = string.replace(attribute, ctx.guild.id)
    #     if attribute == "[server.memberCount]":
    #         string = string.replace(attribute, ctx.guild.member_count)
    #     if attribute == "[server.owner]":
    #         string = string.replace(attribute, str(ctx.guild.owner))
    #     if attribute == "[server.owner.id]":
    #         string = string.replace(attribute, ctx.guild.owner)
    print(string)
    return string