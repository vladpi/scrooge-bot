from typing import TYPE_CHECKING, Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .. import buttons

if TYPE_CHECKING:
    from aiogram import Bot


async def main_menu(
    bot: 'Bot',
    to_chat_id: int,
    text: Optional[str] = None,
    has_transactions: bool = True,
):
    if text is None:
        text = '<b>Ты в главном меню!</b>'

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
