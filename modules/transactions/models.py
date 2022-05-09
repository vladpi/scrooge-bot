from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from libs.base_model import BaseModel
from modules.accounts import Account
from modules.categories import Category
from modules.core.consts import Currency


class Transaction(BaseModel):
    id: int
    user_id: int

    at_date: date
    category_id: int
    category: Category
    comment: Optional[str]

    income_account_id: Optional[int]
    income_account: Optional[Account]
    income_currency: Optional[Currency]
    income: Optional[Decimal]

    outcome_account_id: Optional[int]
    outcome_account: Optional[Account]
    outcome_currency: Optional[Currency]
    outcome: Optional[Decimal]

    created_at: datetime
    updated_at: datetime

    def __str__(self):
        # FIXME ???
        parts = [
            part
            for part in [
                f'<b>Сумма:</b> {self.outcome}',
                f'<b>Комментарий:</b> {self.comment}' if self.comment else None,
                f'<b>Категория:</b> {self.category.name}',
            ]
            if part is not None
        ]

        return '\n'.join(parts)
