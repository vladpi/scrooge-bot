from datetime import datetime

from libs.base_model import BaseModel


class Category(BaseModel):
    id: int
    user_id: int

    name: str

    is_income: bool
    is_outcome: bool

    created_at: datetime
    updated_at: datetime
