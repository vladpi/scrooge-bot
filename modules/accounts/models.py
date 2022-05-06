from libs.base_model import BaseModel


class Account(BaseModel):
    id: int
    owner_id: int
    name: str
