from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .consts import TransactionType


class TransactionSchema(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: Decimal
    comment: Optional[str]
    on_date: date
    category: str

    def __str__(self):
        from bot.resources import messages  # FIXME

        parts = [
            part
            for part in [
                messages.EXPENSE_AMOUNT.format(amount=self.amount),
                messages.EXPENSE_COMMENT.format(comment=self.comment) if self.comment else None,
                messages.EXPENSE_CATEGORY.format(category=self.category),
            ]
            if part is not None
        ]

        return '\n'.join(parts)
