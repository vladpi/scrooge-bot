from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app import database
from libs.base_repo import BaseModelRepository

from .models import Account
from .tables import accounts, accounts_users


class AccountRepository(BaseModelRepository[Account]):
    async def add_user(self, id_: int, user_id: int) -> None:
        # FIXME
        query = insert(accounts_users).values(account_id=id_, user_id=user_id)
        await self.db.execute(query)

    def _by_user_query(self, user_id: int):
        return (
            select([accounts])
            .where(
                accounts_users.c.user_id == user_id,
            )
            .select_from(
                accounts.join(accounts_users),
            )
        )

    async def get_by_user(self, user_id: int) -> List[Account]:
        query = self._by_user_query(user_id)
        return await self._fetch_all(query)

    async def get_by_user_and_name(self, user_id: int, name: str) -> Optional[Account]:
        query = self._by_user_query(user_id).where(accounts.c.name == name).limit(1)
        return await self._fetch_one(query)


accounts_repo = AccountRepository(
    db=database,
    model_class=Account,
    table=accounts,
    pk_field=accounts.c.id,
)
