from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select
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

    async def get_for_user(self, user_id: int) -> List['TransactionSchema']:
        query = select([transactions]).where(transactions.c.user_id == user_id)

        records = await self.db.fetch_all(query)

        return [TransactionSchema.parse_obj(record) for record in records]


transaction_service = TransactionService()
