from aiogram import Bot, Dispatcher
import asyncio
import aiohttp
import logging
from config import BOT_TOKEN
from handlers import router
from aiogram.client.default import DefaultBotProperties


async def main():
    async with aiohttp.ClientSession() as session:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s %(message)s')
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='html'))
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot, session=session)


if __name__ == '__main__':
    asyncio.run(main())