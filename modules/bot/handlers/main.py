from typing import TYPE_CHECKING

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from modules.transactions import count_transactions_by_user

from .. import views
from ..bot import dispatcher

if TYPE_CHECKING:
    from modules.users import UserSchema


@dispatcher.message_handler(filters.CommandStart(), state='*')
async def start(message: types.Message, state: FSMContext, user: 'UserSchema'):
    has_transactions = await count_transactions_by_user(user.id) > 0
    await state.reset_state()
    await views.main.main_menu(message.chat.id, has_transactions=has_transactions)
