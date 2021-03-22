from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Union

from const import TransactionType

from .schemas import TransactionSchema
from .service import transaction_service


async def create_expense_transaction(
    user_id: int,
    account_id: int,
    amount: Decimal,
    comment: Optional[str],
    on_date: Union[date, str],
    category: str,
) -> TransactionSchema:
    if isinstance(on_date, str):
        on_date = datetime.strptime(on_date, '%d.%m.%Y').date()

    return await transaction_service.create(
        user_id=user_id,
        account_id=account_id,
        type_=TransactionType.EXPENSE,
        amount=amount,
        comment=comment,
        on_date=on_date,
        category=category,
    )


async def count_transactions_by_user(user_id: int) -> int:
    return await transaction_service.count_for_user(user_id)


async def get_transactions_by_user(
    user_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TransactionSchema]:
    return await transaction_service.get_for_user(user_id=user_id, limit=limit, offset=offset)
