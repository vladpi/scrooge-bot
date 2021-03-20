from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: int
    owner_id: int
    name: str
