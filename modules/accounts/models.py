from datetime import datetime
from decimal import Decimal

from libs.base_model import BaseModel
from modules.core import Currency


class Account(BaseModel):
    id: int
    owner_id: int

    name: str

    balance: Decimal
    currency: Currency

    created_at: datetime
    updated_at: datetime
