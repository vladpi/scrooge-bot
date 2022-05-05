import abc
from typing import TYPE_CHECKING, Any, Generic, Optional, Type, TypeVar

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .base_model import BaseModel
from .model_factory import factory

if TYPE_CHECKING:
    from databases import Database

Model = TypeVar('Model', bound=BaseModel)


class BaseSQLRepository(Generic[Model], metaclass=abc.ABCMeta):
    def __init__(
        self,
        db: 'Database',
        model_class: Type['Model'],
        table: sa.Table,
        pk_field: sa.Column,
    ):
        self.db = db
        self.model_class = model_class
        self.table = table
        self.pk_field = pk_field

    async def create(self, **data: Any) -> 'Model':
        async with self.db.transaction():
            return await self._fetch_one(  # type: ignore
                insert(self.table).values(data).returning(self.table)
            )

    async def save(self, instance: 'Model') -> 'Model':
        async with self.db.transaction():
            instance_data = factory.dump(instance)
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

    async def delete(self, id_: Any) -> None:
        query = sa.delete(self.table).where(self.pk_field == id_)

        await self.db.execute(query)

    async def _fetch_one(self, query: sa.sql.ClauseElement) -> Optional['Model']:
        record = await self.db.fetch_one(query)
        if record is None:
            return None
        return factory.load(record, self.model_class)
