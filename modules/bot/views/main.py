from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from ..bot import bot
from ..resources import buttons, messages


async def main_menu(
    to_chat_id: int,
    text: Optional[str] = None,
    has_transactions: bool = True,
):
    if text is None:
        text = messages.MAIN_MENU

    keyboard = [
        [KeyboardButton(buttons.ADD_EXPENSE)],
        [KeyboardButton(buttons.HISTORY), KeyboardButton(buttons.REPORTS)]
        if has_transactions
        else [],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id,
        text=text,
        reply_markup=reply_markup,
    )
