#imports
import asyncio
import os
from quart import Quart, render_template, redirect, url_for

#create instance of Quart
app = Quart(__name__)

#return the index.html file with variables
@app.route("/")
async def index():
    return await render_template("./index.html", botName="Mr. Bot", botOwner="dead..#7420", botLoginUrl=url_for("login"), botInviteUrl=url_for("invite"), botServer=url_for("server"))

#create the /invite endpoint
@app.route("/invite")
async def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=1033024808146964571&scope=bot%20applications.commands&permissions=1513962695871")

#create the login endpoint
@app.route("/login")
async def login():
    return "haven't added it yet lol"

#create the server endpoint
@app.route("/server")
async def server():
    return "k ?"

#run function to be imported in main.py
async def run():
    await app.run_task()