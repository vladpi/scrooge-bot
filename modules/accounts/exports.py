from typing import List

from .schemas import AccountSchema
from .service import account_service


async def create_account(user_id: int, name: str) -> AccountSchema:
    account = await account_service.create(user_id, name)
    await account_service.add_user(account.id, user_id)
    return account


async def get_user_accounts(user_id: int) -> List[AccountSchema]:
    return await account_service.get_by_user(user_id)
