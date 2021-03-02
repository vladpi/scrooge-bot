from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from db.tables import expenses
from schemas.expense import ExpenseSchema
from services.base import BaseDBService


class ExpenseService(BaseDBService):
    async def put(self, instance: 'ExpenseSchema') -> 'ExpenseSchema':
        query = (
            insert(expenses)
                .values(instance.dict())
                .on_conflict_do_update(
                index_elements=[expenses.c.id],
                set_=instance.dict(exclude={'id', 'user_id', 'created_at'}),
            )
                .returning(expenses)
        )

        record = await self.db.fetch_one(query)

        return ExpenseSchema.parse_obj(record)

    async def create(
            self,
            user_id: int,
            amount: Decimal,
            comment: Optional[str],
            on_date: date,
            category: str,
    ) -> 'ExpenseSchema':
        query = insert(expenses).values(
            user_id=user_id,
            amount=amount,
            comment=comment,
            on_date=on_date,
            category=category,
        ).returning(expenses)

        record = await self.db.fetch_one(query)

        return ExpenseSchema.parse_obj(record)


expense_service = ExpenseService()
