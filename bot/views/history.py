from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import bot
from bot.const import history_cb
from modules.transactions import TransactionSchema


async def history(
    to_chat_id: int,
    expenses: List[TransactionSchema],
    current_page: int = 0,
    total_pages: int = 0,
    message_for_update: Optional[Message] = None,
):
    message = '\n\n'.join([str(exp) for exp in expenses])

    reply_markup = InlineKeyboardMarkup()

    if current_page > 0:
        reply_markup.insert(
            InlineKeyboardButton('◀️', callback_data=history_cb.new(page=current_page - 1)),
        )

    if current_page < total_pages:
        reply_markup.insert(
            InlineKeyboardButton('▶️', callback_data=history_cb.new(page=current_page + 1)),
        )

    if message_for_update is not None:
        await message_for_update.edit_text(
            text=message,
            reply_markup=reply_markup,
        )

    else:
        await bot.send_message(
            chat_id=to_chat_id,
            text=message,
            reply_markup=reply_markup,
        )
