def addGuildsToDatabase(guildIds: list, data: dict):
    for id in guildIds:
        data[int(id)] = {"prefix": "?", "stripAfterPrefix": False}
    return data