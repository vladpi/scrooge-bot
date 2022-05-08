from .consts import CATEGORIES
from .models import Category
from .repository import categories_repo


async def create_default_categories(user_id: int) -> list[Category]:
    return [
        await categories_repo.create(
            user_id=user_id,
            name=category_name,
        )
        for category_name in CATEGORIES
    ]


async def get_user_categories(user_id: int) -> list[Category]:
    return await categories_repo.get_all_by_user_id(user_id)


async def get_user_category_by_name(user_id: int, name: str) -> Category | None:
    return await categories_repo.get_by_name(user_id, name)
