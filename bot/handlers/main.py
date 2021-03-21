from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from bot import dispatcher, views


@dispatcher.message_handler(filters.CommandStart(), state='*')
async def start(message: types.Message, state: FSMContext):
    await state.reset_state()
    await views.main.main_menu(message.chat.id)
