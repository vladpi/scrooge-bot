from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import views


async def start(message: types.Message, state: FSMContext):
    await state.reset_state()
    await views.main.main_menu(message.chat.id)
