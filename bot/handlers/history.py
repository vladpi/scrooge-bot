import logging
from math import ceil
from typing import TYPE_CHECKING, Dict

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import views
from services.transactions import transaction_service

if TYPE_CHECKING:
    from schemas.user import UserSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TRANSACTION_PER_PAGE = 50


async def history_entry(message: types.Message, state: FSMContext, user: 'UserSchema'):
    total = await transaction_service.count_for_user(user.id)
    expenses = await transaction_service.get_for_user(user.id, limit=TRANSACTION_PER_PAGE)

    if not expenses:
        # FIXME сообщение о пустых расходах
        return

    await views.history.history(
        user.id,
        expenses,
        total_pages=int(ceil(total / float(TRANSACTION_PER_PAGE))) - 1,
    )


async def history_page(
    query: types.CallbackQuery,
    callback_data: Dict[str, str],
    user: 'UserSchema',
):
    page = int(callback_data.get('page', 0))

    total = await transaction_service.count_for_user(user.id)
    expenses = await transaction_service.get_for_user(
        user.id,
        limit=TRANSACTION_PER_PAGE,
        offset=page * TRANSACTION_PER_PAGE,
    )

    if not expenses:
        return

    await views.history.history(
        user.id,
        expenses,
        current_page=page,
        total_pages=int(ceil(total / float(TRANSACTION_PER_PAGE))) - 1,
        message_for_update=query.message,
    )
    await query.answer()
