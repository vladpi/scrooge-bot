import logging

from aiogram import executor

from bot.dispatcher import dispatcher, register_handlers

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    register_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True)
