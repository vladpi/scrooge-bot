from decimal import Decimal
from typing import List, Optional

from modules.core import Currency

from .consts import DEFAULT_ACCOUNT_CURRENCY, DEFAULT_ACCOUNT_NAME
from .models import Account
from .repository import accounts_repo


async def create_default_account(user_id: int) -> Account:
    return await create_account(
        user_id=user_id,
        name=DEFAULT_ACCOUNT_NAME,
        currency=DEFAULT_ACCOUNT_CURRENCY,
    )


async def create_account(
    user_id: int,
    name: str,
    currency: Currency,
    balance: Decimal | int | float = 0,
) -> Account:
    account = await accounts_repo.create(
        owner_id=user_id,
        name=name,
        balance=balance,
        currency=currency,
    )
    await accounts_repo.add_user(account.id, user_id)
    return account


async def get_user_accounts(user_id: int) -> List[Account]:
    return await accounts_repo.get_by_user(user_id)


async def get_user_account_by_name(user_id: int, name: str) -> Optional[Account]:
    return await accounts_repo.get_by_user_and_name(user_id, name)
