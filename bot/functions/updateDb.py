import json
from discord.ext.commands import Bot
from bot.functions.addGuildsToDb import addGuildsToDb

def updateDb(bot: Bot):
    with open("data.json", mode="r") as f:
        data: dict = json.load(f)
    with open("updates.json", mode="r") as f:
        exp: dict = json.load(f)
    keys = exp.keys()
    for key in data:
        for updatedKey in keys:
            data[key][updatedKey] = exp[updatedKey]
    unAddedGuilds = []
    for guild in bot.guilds:
        if not str(guild.id) in data:
            unAddedGuilds.append(guild.id)
    data = addGuildsToDb(unAddedGuilds, data=data)
    exp.clear()
    with open("updates.json", mode="w") as f:
        json.dump(exp, f, indent=4)
    with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)
    return