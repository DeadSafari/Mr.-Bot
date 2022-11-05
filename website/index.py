#imports
import asyncio
import os
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import discord

#create instance of Quart
app = Quart(__name__)

app.secret_key = b"yesyesyes"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = 1033024808146964571
app.config["DISCORD_CLIENT_SECRET"] = "bvP96KmyC-en8-7NDaAoWoRIE5CreVCi"
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
        serverCount=5000,
        userCount="10,000",
        commandCount="500,000"
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


@app.route("/dashboard")
async def dashboard():
    user = await discord.fetch_user()
    return await render_template("dashboard.html", user=user)

async def run():
    await app.run_task(
        host="0.0.0.0",
        port=os.getenv("PORT")
    )