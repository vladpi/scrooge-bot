from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
