from datetime import date
from decimal import Decimal
from typing import Optional

from libs.base_model import BaseModel

from .consts import TransactionType


class Transaction(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: Decimal
    comment: Optional[str]
    on_date: date
    category: str

    def __str__(self):
        # FIXME ???
        parts = [
            part
            for part in [
                f'<b>Сумма:</b> {self.amount}',
                f'<b>Комментарий:</b> {self.comment}' if self.comment else None,
                f'<b>Категория:</b> {self.category}',
            ]
            if part is not None
        ]

        return '\n'.join(parts)
