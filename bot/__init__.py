from .bot import bot
from .dispatcher import dispatcher, register_handlers, register_middlewares

__all__ = [
    'bot',
    'dispatcher',
    'register_handlers',
    'register_middlewares',
]
