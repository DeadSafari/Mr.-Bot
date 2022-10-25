#imports
from website.index import run
from bot.bot import main
import asyncio
import threading

#start function
async def start():
    #create an instance of Thread to start main function
    thread = threading.Thread(target=asyncio.run, args=[main()])
    #start the instance of Thread
    thread.start()
    #await the run function for webserver
    await run() 

#start an event loop
asyncio.run(start())