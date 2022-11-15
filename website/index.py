#imports
import asyncio
import datetime
import os
import time
from quart import Quart, render_template, redirect, url_for, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc, commands
import discord
from bot.botMain import return_bot

    

#create instance of Quart
app = Quart(__name__)

app.config['SECRET_KEY'] = "yesyesyes"
app.config["DISCORD_CLIENT_ID"] = 1033024808146964571
app.config["DISCORD_CLIENT_SECRET"] = "NPAssioS3ROtc5kOS5OUOuGighXk3npH"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = "MTAzMzAyNDgwODE0Njk2NDU3MQ.G2dlAL.0qdXOjAE_0OELzg7MTQ_ywqfO5MW0h4wpn6vW4"
discord = DiscordOAuth2Session(app)

@app.route("/")
async def index():
    return await render_template(
        "index.html",
        botName="Mr. Bot",
        urlForCommands=url_for("commands"),
        inviteUrl=url_for("invite"),
        supportServer=url_for('server'),
        serverCount=len(app.bot.guilds),
        userCount=len(app.bot.users),
        upTime=str(datetime.timedelta(seconds=int(round(time.time()-app.bot.startTime))))
    )

@app.route("/commands")
async def commands():
    return await render_template("/pages/commands.html",
    botName="Mr. Bot",
    homePage=url_for("index"),
    inviteUrl=url_for("invite"),
    supportServer=url_for('server')
    )


#create the /invite endpoint
@app.route("/invite")
async def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=1033024808146964571&scope=bot%20applications.commands&permissions=1513962695871")

@app.route("/server")
async def server():
    return redirect('https://discord.gg/U7GmAKFn2c')

#create the login endpoint
@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=['POST', 'GET'])
async def dashboard():
    if request.method == "POST":
        output = request.form.to_dict()
        if request.form['commandData'] == "updated":
            print(request.form)
            print(output)

    user = await discord.fetch_user()
    with open("./website/templates/pages/banCmd.html", "r") as file:
        banCmd = file.read()
    return await render_template("/pages/dashboard.html", user=user, banCmd=banCmd)

@app.route("/succesDbUpdate", methods=['GET', 'POST'])
async def succesDbUpdate():
    if request.method == "POST":
        return "k"
    elif request.method == "GET":
        return "k ?"


async def run():
    app.bot = return_bot()
    await app.run_task(
        host="0.0.0.0",
        port=5000
    )