import abc
from typing import TYPE_CHECKING, Any, Generic, List, Optional, Type, TypeVar

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .base_model import BaseModel

if TYPE_CHECKING:
    from databases import Database

Model = TypeVar('Model', bound=BaseModel)


class BaseRepository(Generic[Model], metaclass=abc.ABCMeta):
    def __init__(
        self,
        db: 'Database',
        model_class: Type['Model'],
    ):
        self.db = db
        self.model_class = model_class

    async def _fetch_one(self, query: sa.sql.ClauseElement) -> Optional['Model']:
        record = await self.db.fetch_one(query)
        if record is None:
            return None
        return self.model_class.parse_obj(record)

    async def _fetch_all(self, query: sa.sql.ClauseElement) -> List['Model']:
        records = await self.db.fetch_all(query)
        return [self.model_class.parse_obj(record) for record in records]


class BaseModelRepository(BaseRepository[Model]):
    def __init__(
        self,
        db: 'Database',
        model_class: Type['Model'],
        table: sa.Table,
        pk_field: sa.Column,
    ):
        super().__init__(db, model_class)
        self.table = table
        self.pk_field = pk_field

    async def create(self, **data: Any) -> 'Model':
        async with self.db.transaction():
            return await self._fetch_one(  # type: ignore
                insert(self.table).values(data).returning(self.table)
            )

    async def save(self, instance: 'Model') -> 'Model':
        async with self.db.transaction():
            instance_data = instance.dict()
            pk_value = instance_data.pop(self.pk_field.key)
            return await self._fetch_one(  # type: ignore
                sa.update(self.table)
                .where(self.pk_field == pk_value)
                .values(instance_data)
                .returning(self.table)
            )

    async def get(self, id_: Any) -> Optional['Model']:
        return await self._fetch_one(sa.select([self.table]).where(self.pk_field == id_))

    async def get_by(self, column: sa.Column, value: Any) -> Optional['Model']:
        return await self._fetch_one(sa.select([self.table]).where(column == value))

    async def get_all_by(self, column: sa.Column, value: Any) -> List['Model']:
        return await self._fetch_all(sa.select([self.table]).where(column == value))

    async def delete(self, id_: Any) -> None:
        query = sa.delete(self.table).where(self.pk_field == id_)

        await self.db.execute(query)
