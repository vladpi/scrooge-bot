from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from .models import Transaction
from .repository import transactions_repo

if TYPE_CHECKING:
    from modules.core.consts import Currency


async def create_outcome_transaction(
    user_id: int,
    at_date: Union[date, str],
    category_id: int,
    comment: Optional[str],
    account_id: int,
    currency: 'Currency',
    amount: Decimal,
) -> Transaction:
    if isinstance(at_date, str):
        at_date = datetime.strptime(at_date, '%d.%m.%Y').date()

    return await transactions_repo.create(
        user_id=user_id,
        at_date=at_date,
        category_id=category_id,
        comment=comment,
        outcome_account_id=account_id,
        outcome_currency=currency,
        outcome=amount,
    )


async def count_transactions_by_user(user_id: int) -> int:
    return await transactions_repo.count_for_user(user_id)


async def get_transactions_by_user(
    user_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Transaction]:
    return await transactions_repo.get_for_user(user_id=user_id, limit=limit, offset=offset)


async def get_transactions_history(
    user_id: int,
    at_date: Optional[date] = None,
) -> Tuple[Optional[date], Optional[date], Optional[date], List[Transaction]]:
    prev_date, at_date, next_date = await transactions_repo.get_dates_for_user(user_id, at_date)

    if at_date is None:
        return None, None, None, []

    transactions = await transactions_repo.get_for_user(user_id=user_id, at_date=at_date)

    return prev_date, at_date, next_date, transactions
