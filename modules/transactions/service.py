from asyncio import gather
from datetime import date
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import distinct, func, select
from sqlalchemy.dialects.postgresql import insert

from const import TransactionType
from libs.base_service import BaseDBService
from modules.db.tables import transactions

from .schemas import TransactionSchema


class TransactionService(BaseDBService):
    async def put(self, instance: 'TransactionSchema') -> 'TransactionSchema':
        query = (
            insert(transactions)
            .values(instance.dict())
            .on_conflict_do_update(
                index_elements=[transactions.c.id],
                set_=instance.dict(exclude={'id', 'user_id', 'created_at'}),
            )
            .returning(transactions)
        )

        record = await self.db.fetch_one(query)

        return TransactionSchema.parse_obj(record)

    async def create(
        self,
        user_id: int,
        account_id: int,
        type_: TransactionType,
        amount: Decimal,
        comment: Optional[str],
        on_date: date,
        category: str,
    ) -> 'TransactionSchema':
        query = (
            insert(transactions)
            .values(
                user_id=user_id,
                account_id=account_id,
                type=type_,
                amount=amount,
                comment=comment,
                on_date=on_date,
                category=category,
            )
            .returning(transactions)
        )

        record = await self.db.fetch_one(query)

        return TransactionSchema.parse_obj(record)

    async def get_for_user(
        self,
        user_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        on_date: Optional[date] = None,
    ) -> List['TransactionSchema']:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .order_by(transactions.c.on_date.desc(), transactions.c.created_at.desc(),)
        )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        if on_date is not None:
            query = query.where(transactions.c.on_date == on_date)

        records = await self.db.fetch_all(query)

        return [TransactionSchema.parse_obj(record) for record in records]

    async def count_for_user(self, user_id: int) -> int:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .with_only_columns([func.count()])
        )
        return await self.db.execute(query)

    async def get_dates_for_user(
        self, user_id: int, current_date: Optional[date] = None
    ) -> Tuple[Optional[date], Optional[date], Optional[date]]:
        if current_date is None:
            query = select([func.max(transactions.c.on_date)]).where(
                transactions.c.user_id == user_id
            )
            current_date = await self.db.fetch_val(query)

        if current_date is None:
            return None, None, None

        prev_query = select([func.max(transactions.c.on_date)]).where(
            transactions.c.user_id == user_id, transactions.c.on_date < current_date,
        )
        next_query = select([func.min(transactions.c.on_date)]).where(
            transactions.c.user_id == user_id, transactions.c.on_date > current_date,
        )

        prev_date, next_date = await gather(
            self.db.fetch_val(prev_query), self.db.fetch_val(next_query)
        )

        return prev_date, current_date, next_date


transaction_service = TransactionService()
