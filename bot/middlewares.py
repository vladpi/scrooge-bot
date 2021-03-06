from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from services.users import user_service


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['user'] = await self._register_user(message.from_user)

    async def on_process_callback_query(self, callback_query: types.Message, data: dict):
        data['user'] = await self._register_user(callback_query.from_user)

    async def _register_user(self, from_user: types.User):
        return await user_service.create_or_update(
            from_user.id,
            from_user.username,
            from_user.first_name,
            from_user.last_name,
        )
