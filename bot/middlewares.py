from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from const import DEFAULT_ACCOUNT_NAME
from modules.users import user_service
from modules.accounts import account_service


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['user'] = await self._fetch_user(message.from_user)

    async def on_process_callback_query(self, callback_query: types.Message, data: dict):
        data['user'] = await self._fetch_user(callback_query.from_user)

    async def _fetch_user(self, from_user: types.User):
        user = await user_service.get(from_user.id)

        if user is None:
            user = await user_service.create(
                from_user.id,
                from_user.username,
                from_user.first_name,
                from_user.last_name,
            )

            account = await account_service.create(user.id, DEFAULT_ACCOUNT_NAME)
            await account_service.add_user(account.id, user.id)

        else:
            user.username = from_user.username
            user.first_name = from_user.first_name
            user.last_name = from_user.last_name
            user = await user_service.put(user)

        return user
