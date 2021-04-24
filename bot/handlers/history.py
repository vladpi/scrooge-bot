import logging
from datetime import date, datetime
from typing import TYPE_CHECKING, Dict, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from app import dispatcher
from bot import views
from bot.const import history_cb
from bot.resources import buttons
from modules.transactions import get_transactions_history

if TYPE_CHECKING:
    from modules.users import UserSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dispatcher.message_handler(filters.Text(equals=buttons.HISTORY))
async def history_entry(message: types.Message, state: FSMContext, user: 'UserSchema'):
    prev_date, current_date, next_date, expenses = await get_transactions_history(user.id)

    if not expenses or current_date is None:
        # FIXME сообщение о пустых расходах
        return

    await views.history.history(
        user.id, current_date, expenses, next_date=next_date, prev_date=prev_date,
    )


@dispatcher.callback_query_handler(history_cb.filter())
async def history_page(
    query: types.CallbackQuery, callback_data: Dict[str, str], user: 'UserSchema',
):
    try:
        on_date: Optional[date] = datetime.strptime(callback_data.get('date'), '%d.%m.%Y').date()
    except ValueError:
        on_date = None

    prev_date, current_date, next_date, expenses = await get_transactions_history(
        user.id, on_date=on_date
    )

    if not expenses or current_date is None:
        return

    await views.history.history(
        user.id,
        current_date,
        expenses,
        next_date=next_date,
        prev_date=prev_date,
        message_for_update=query.message,
    )
    await query.answer()
