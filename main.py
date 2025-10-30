import asyncio
import logging
from database.api import exec
from database.querys import query
from bot.service import start_polling
import bot.handlers

logging.basicConfig(level=logging.INFO)

async def main():
    await exec(query["create table"])
    await start_polling()

if __name__ == "__main__":
    asyncio.run(main())