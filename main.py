import logging

from aiogram import executor
from aiogram.dispatcher import Dispatcher

from bot import dispatcher
from bot.middlewares import UserMiddleware
from modules.db import database

logging.basicConfig(level=logging.INFO)


async def on_startup(dp: Dispatcher):
    dp.middleware.setup(UserMiddleware())
    await database.connect()


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True,
    )
