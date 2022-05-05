from app import settings

from .bot import bot
# from .consts import COMMANDS


async def setup() -> None:
    url = f'{settings.WEBHOOK_HOST}/tg/webhook/{settings.TG_BOT_TOKEN.get_secret_value()}'
    # current_url = (await bot.get_webhook_info())['url']
    # if current_url != url:
    await bot.set_webhook(url=url, drop_pending_updates=True)
    # await bot.set_my_commands(COMMANDS)
