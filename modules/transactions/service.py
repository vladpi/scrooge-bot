from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func, select
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
