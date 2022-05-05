from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode

from app import settings

from .middlewares import UserMiddleware

bot = Bot(
    token=settings.TG_BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML,
)

storage = RedisStorage2(
    host=settings.REDIS_URL.host,
    port=settings.REDIS_URL.port,
    password=settings.REDIS_URL.password,
    db=int(settings.REDIS_URL.path.replace('/', '')),  # type: ignore
)

dispatcher: Dispatcher = Dispatcher(bot, storage=storage)
dispatcher.setup_middleware(UserMiddleware())

from .views import *  # noqa
from .handlers import *  # noqa
