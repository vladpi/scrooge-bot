from datetime import date
from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app import bot
from bot.const import history_cb
from modules.transactions import TransactionSchema


async def history(
    to_chat_id: int,
    current_date: date,
    expenses: List[TransactionSchema],
    next_date: Optional[date] = None,
    prev_date: Optional[date] = None,
    message_for_update: Optional[Message] = None,
):
    message = f'<b>{current_date:%d.%m.%Y}</b>\n\n'
    message += '\n\n'.join([str(exp) for exp in expenses])

    reply_markup = InlineKeyboardMarkup()

    if prev_date is not None:
        reply_markup.insert(
            InlineKeyboardButton(
                '◀️', callback_data=history_cb.new(date=prev_date.strftime('%d.%m.%Y'))
            ),
        )

    if next_date is not None:
        reply_markup.insert(
            InlineKeyboardButton(
                '▶️', callback_data=history_cb.new(date=next_date.strftime('%d.%m.%Y'))
            ),
        )

    if message_for_update is not None:
        await message_for_update.edit_text(
            text=message, reply_markup=reply_markup,
        )

    else:
        await bot.send_message(
            chat_id=to_chat_id, text=message, reply_markup=reply_markup,
        )
