from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from bot.resources import messages


class ExpenseSchema(BaseModel):
    amount: Decimal
    comment: Optional[str]
    on_date: date
    category: str

    def __str__(self):
        parts = [
            part
            for part in [
                messages.EXPENSE_AMOUNT.format(amount=self.amount),
                messages.EXPENSE_COMMENT.format(comment=self.comment)
                if self.comment
                else None,
                messages.EXPENSE_DATE.format(date=self.on_date),
                messages.EXPENSE_CATEGORY.format(category=self.category),
            ]
            if part is not None
        ]

        return '\n'.join(parts)
