from website.index import run
from bot.bot import main
import asyncio
import threading

async def start():
    thread = threading.Thread(target=asyncio.run, args=[main()])
    thread.start()
    await run() 


asyncio.run(start())