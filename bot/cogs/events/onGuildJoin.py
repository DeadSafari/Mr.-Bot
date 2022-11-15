import json
import discord
from discord.ext import commands

class onGuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("cogs.events.onGuildJoin is now ready!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        with open("data.json", "r") as f:
            data: dict = json.load(f)
        
        with open("base.json", mode="r") as f:
            baseData = json.load(f)
        
        data[str(guild.id)] = baseData

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

        for channel in guild.channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Hello! I'm still in development, so please be patient with me! For a list of commands, goto https://www.mr-bot.ml/commands to get a list of current commands.")
                return
        try:
            await guild.owner.send("Hello! I'm still in development, the customization on the backend is ready, it just needs to be linked to the website to be started. So please be patient with me! For a list of commands that are currently available, goto https://www.mr-bot.ml/commands to get a list of current commands.")
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(onGuildJoin(bot))            