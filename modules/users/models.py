from datetime import datetime
from typing import Optional

from libs.base_model import BaseModel


class User(BaseModel):
    id: int

    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    created_at: datetime
    updated_at: datetime
