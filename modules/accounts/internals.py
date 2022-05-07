from typing import List, Optional

from .models import Account
from .repository import accounts_repo


async def create_account(user_id: int, name: str) -> Account:
    account = await accounts_repo.create(user_id=user_id, name=name)
    await accounts_repo.add_user(account.id, user_id)
    return account


async def get_user_accounts(user_id: int) -> List[Account]:
    return await accounts_repo.get_by_user(user_id)


async def get_user_account_by_name(user_id: int, name: str) -> Optional[Account]:
    return await accounts_repo.get_by_user_and_name(user_id, name)
