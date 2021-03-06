from datetime import date
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from const import TransactionType
from db.tables import transactions
from schemas.transaction import TransactionSchema
from services.base import BaseDBService


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
        type: TransactionType,
        amount: Decimal,
        comment: Optional[str],
        on_date: date,
        category: str,
    ) -> 'TransactionSchema':
        query = (
            insert(transactions)
            .values(
                user_id=user_id,
                type=type,
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
    ) -> List['TransactionSchema']:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .order_by(transactions.c.on_date.desc())
        )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        records = await self.db.fetch_all(query)

        return [TransactionSchema.parse_obj(record) for record in records]

    async def count_for_user(self, user_id: int) -> int:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .with_only_columns([func.count()])
        )
        return await self.db.execute(query)


transaction_service = TransactionService()
