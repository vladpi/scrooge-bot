from aiogram import Bot, Dispatcher

from .bot import bot, dispatcher


async def get_bot_dispatcher() -> Dispatcher:
    Bot.set_current(bot)
    Dispatcher.set_current(dispatcher)
    return dispatcher
