import logging

from aiogram import executor
from alembic.util import Dispatcher

from bot.dispatcher import dispatcher, register_handlers
from db import database

logging.basicConfig(level=logging.INFO)


async def on_startup(dp: Dispatcher):
    register_handlers(dp)
    await database.connect()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_startup, skip_updates=True)
