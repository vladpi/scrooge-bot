import sqlalchemy as sa

from app import database
from libs.base_repo import BaseModelRepository

from .models import Category
from .tables import categories


class CategoryRepository(BaseModelRepository[Category]):
    async def get_all_by_user_id(self, user_id: int) -> list[Category]:
        return await self.get_all_by(self.table.c.user_id, user_id)

    async def get_by_name(self, user_id: int, name: str) -> Category | None:
        query = sa.select([self.table]).where(
            self.table.c.user_id == user_id,
            self.table.c.name == name,
        )
        return await self._fetch_one(query)


categories_repo = CategoryRepository(
    db=database,
    model_class=Category,
    table=categories,
    pk_field=categories.c.id,
)
