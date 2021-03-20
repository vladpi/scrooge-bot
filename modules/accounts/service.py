from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from libs.base_service import BaseDBService
from modules.db.tables import accounts, accounts_users

from .schemas import AccountSchema


class AccountService(BaseDBService):
    async def put(self, instance: 'AccountSchema') -> 'AccountSchema':
        query = (
            insert(accounts)
            .values(instance.dict())
            .on_conflict_do_update(
                index_elements=[accounts.c.id],
                set_=instance.dict(exclude={'id'}),
            )
            .returning(accounts)
        )

        record = await self.db.fetch_one(query)

        return AccountSchema.parse_obj(record)

    async def create(
        self,
        owner_id: int,
        name: str,
    ) -> 'AccountSchema':
        query = (
            insert(accounts)
            .values(
                owner_id=owner_id,
                name=name,
            )
            .returning(accounts)
        )

        record = await self.db.fetch_one(query)

        return AccountSchema.parse_obj(record)

    async def get(self, id_: int) -> Optional['AccountSchema']:
        query = sa.select([accounts]).where(
            accounts.c.id == id_,
        )

        record = await self.db.fetch_one(query)

        if record is not None:
            return AccountSchema.parse_obj(record)

    async def add_user(self, id_: int, user_id: int) -> None:
        query = insert(accounts_users).values(
            account_id=id_,
            user_id=user_id,
        )

        await self.db.execute(query)

        return None

    async def get_by_user(self, user_id: int) -> List[AccountSchema]:
        query = (
            select([accounts])
            .where(
                accounts_users.c.user_id == user_id,
            )
            .select_from(
                accounts.join(accounts_users),
            )
        )

        records = await self.db.fetch_all(query)

        return [AccountSchema.parse_obj(record) for record in records]


account_service = AccountService()
