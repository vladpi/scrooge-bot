from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot import bot
from bot.resources import buttons, messages


async def main_menu(to_chat_id: int, text: Optional[str] = None):
    if text is None:
        text = messages.MAIN_MENU

    keyboard = [
        [KeyboardButton(buttons.ADD_EXPENSE)],
        [KeyboardButton(buttons.HISTORY)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id, text=text, reply_markup=reply_markup,
    )
