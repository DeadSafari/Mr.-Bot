import os
from quart import Quart, render_template, redirect, url_for

app = Quart(__name__)

@app.route("/")
async def index():
    return await render_template("./index.html", botName="Mr. Bot", botOwner="dead..#7420", botLoginUrl=url_for("login"), botInviteUrl=url_for("invite"), botServer=url_for("server"))

@app.route("/invite")
async def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=1033024808146964571&scope=bot%20applications.commands&permissions=1513962695871")

@app.route("/login")
async def login():
    return "haven't added it yet lol"

@app.route("/server")
async def server():
    return "k ?"

app.run(debug=True)