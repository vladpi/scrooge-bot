import logging

from aiogram import executor
from aiogram.dispatcher import Dispatcher

from bot import bot, dispatcher
from bot.middlewares import UserMiddleware
from config import settings
from modules.db import database

logging.basicConfig(level=logging.INFO)


async def on_startup(dp: Dispatcher):
    if settings.WEBHOOK_HOST:
        await bot.set_webhook(f'{settings.WEBHOOK_HOST}{settings.WEBHOOK_PATH}')

    dp.middleware.setup(UserMiddleware())
    await database.connect()


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    print(settings.WEBHOOK_HOST)
    if settings.WEBHOOK_HOST:
        executor.start_webhook(
            dispatcher,
            settings.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT,
        )

    else:
        executor.start_polling(
            dispatcher, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True,
        )
