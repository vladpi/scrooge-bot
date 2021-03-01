from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from services.users import user_service


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user = await user_service.create_or_update(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        data['user'] = user
