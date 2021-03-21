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


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_startup, skip_updates=True)
