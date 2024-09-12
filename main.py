import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from app.scheduler import start_scheduler
from app.database.models import async_main


async def main():
    load_dotenv()
    await async_main()
    token = os.getenv("TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    start_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
