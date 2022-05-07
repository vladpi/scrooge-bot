from asyncio import gather
from datetime import date
from typing import List, Optional, Tuple

from sqlalchemy import func, select

from app import database
from libs.base_repo import BaseModelRepository

from .models import Transaction
from .tables import transactions


class TransactionRepository(BaseModelRepository[Transaction]):
    async def get_for_user(
        self,
        user_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        on_date: Optional[date] = None,
    ) -> List['Transaction']:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .order_by(
                transactions.c.on_date.desc(),
                transactions.c.created_at.desc(),
            )
        )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        if on_date is not None:
            query = query.where(transactions.c.on_date == on_date)

        records = await self.db.fetch_all(query)

        return [Transaction.parse_obj(record) for record in records]

    async def count_for_user(self, user_id: int) -> int:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .with_only_columns([func.count()])
        )
        return await self.db.execute(query)

    async def get_dates_for_user(
        self,
        user_id: int,
        current_date: Optional[date] = None,
    ) -> Tuple[Optional[date], Optional[date], Optional[date]]:
        if current_date is None:
            query = select([func.max(transactions.c.on_date)]).where(
                transactions.c.user_id == user_id
            )
            current_date = await self.db.fetch_val(query)

        if current_date is None:
            return None, None, None

        prev_query = select([func.max(transactions.c.on_date)]).where(
            transactions.c.user_id == user_id,
            transactions.c.on_date < current_date,
        )
        next_query = select([func.min(transactions.c.on_date)]).where(
            transactions.c.user_id == user_id,
            transactions.c.on_date > current_date,
        )

        prev_date, next_date = await gather(
            self.db.fetch_val(prev_query), self.db.fetch_val(next_query)
        )

        return prev_date, current_date, next_date


transactions_repo = TransactionRepository(
    db=database,
    model_class=Transaction,
    table=transactions,
    pk_field=transactions.c.id,
)