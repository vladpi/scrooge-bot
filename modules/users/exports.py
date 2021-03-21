from typing import Optional

from const import DEFAULT_ACCOUNT_NAME
from modules.accounts import create_account

from .schemas import UserSchema
from .service import user_service


async def create_or_update_user(
    id_: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> UserSchema:
    user = await user_service.get(id_)

    if user is None:
        user = await user_service.create(
            id_=id_,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        await create_account(user.id, DEFAULT_ACCOUNT_NAME)

    else:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user = await user_service.put(user)

    return user


async def get_user(id_: int) -> Optional[UserSchema]:
    return await user_service.get(id_)
