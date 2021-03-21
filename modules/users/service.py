from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from libs.base_service import BaseDBService
from modules.db.tables import users

from .schemas import UserSchema


class UserService(BaseDBService):
    async def put(
        self,
        instance: 'UserSchema',
        allow_update: bool = True,
    ) -> 'UserSchema':
        query = insert(users).values(instance.dict()).returning(users)

        if allow_update:
            query = query.on_conflict_do_update(
                index_elements=[users.c.id],
                set_=instance.dict(exclude={'id', 'created_at'}),
            )

        record = await self.db.fetch_one(query)

        return UserSchema.parse_obj(record)

    async def get(self, id_: int) -> Optional['UserSchema']:
        query = sa.select([users]).where(
            users.c.id == id_,
        )

        record = await self.db.fetch_one(query)

        if record is not None:
            return UserSchema.parse_obj(record)

        return None

    async def create(
        self,
        id_: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> 'UserSchema':
        user = UserSchema(
            id=id_,
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=datetime.utcnow(),
        )

        return await self.put(user, allow_update=False)


user_service = UserService()
