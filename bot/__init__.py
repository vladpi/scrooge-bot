from .core import bot, dispatcher

__all__ = [
    'bot',
    'dispatcher',
]

from .handlers import *  # noqa # isort: skip
