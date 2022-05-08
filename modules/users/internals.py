from asyncio import gather
from typing import Optional

from modules.accounts import create_default_account
from modules.categories import create_default_categories

from .models import User
from .repository import users_repo


async def create_or_update_user(
    id_: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    user = await users_repo.get(id_)

    if user is None:
        user = await users_repo.create(
            id=id_,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        await gather(
            create_default_account(user.id),
            create_default_categories(user.id),
        )

    else:
        user.populate(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user = await users_repo.save(user)

    return user


async def get_user(id_: int) -> Optional[User]:
    return await users_repo.get(id_)
