import logging
from datetime import date, datetime
from typing import TYPE_CHECKING, Dict, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from modules.transactions import get_transactions_history

from ...bot import dispatcher
from .. import buttons
from . import views
from .consts import history_cb

if TYPE_CHECKING:
    from modules.users import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dispatcher.message_handler(filters.Text(equals=buttons.HISTORY))
async def history_entry(message: types.Message, state: FSMContext, user: 'User'):
    prev_date, current_date, next_date, expenses = await get_transactions_history(user.id)

    if not expenses or current_date is None:
        # FIXME сообщение о пустых расходах
        return

    await views.history(
        message.bot,
        user.id,
        current_date,
        expenses,
        next_date=next_date,
        prev_date=prev_date,
    )


@dispatcher.callback_query_handler(history_cb.filter())
async def history_page(
    query: types.CallbackQuery,
    callback_data: Dict[str, str],
    user: 'User',
):
    try:
        at_date: Optional[date] = datetime.strptime(callback_data['date'], '%d.%m.%Y').date()
    except (ValueError, KeyError):
        at_date = None

    prev_date, current_date, next_date, expenses = await get_transactions_history(
        user.id, at_date=at_date
    )

    if not expenses or current_date is None:
        return

    await views.history(
        query.bot,
        user.id,
        current_date,
        expenses,
        next_date=next_date,
        prev_date=prev_date,
        message_for_update=query.message,
    )
    await query.answer()
