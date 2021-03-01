from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from db.tables import users
from schemas.user import UserSchema

from .base import BaseDBService


class UserService(BaseDBService):
    async def put(self, instance: 'UserSchema') -> 'UserSchema':
        query = (
            insert(users)
            .values(instance.dict())
            .on_conflict_do_update(
                index_elements=[users.c.id],
                set_=instance.dict(exclude={'id', 'created_at'}),
            )
            .returning(users)
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

    async def create_or_update(
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

        return await self.put(user)


user_service = UserService()
