from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage

from .settings import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode='html')
storage = RedisStorage(
    host=settings.REDIS_URL.host,
    port=settings.REDIS_URL.port,
    password=settings.REDIS_URL.password,
    db=int(settings.REDIS_URL.path.replace('/', '')),  # type: ignore
)
dispatcher = Dispatcher(bot, storage=storage)
