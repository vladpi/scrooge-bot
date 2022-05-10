from datetime import date
from typing import List

from sqlalchemy import and_, func, literal_column, select

from app import database
from libs.base_repo import BaseRepository
from libs.sql_utils import json_object
from modules.categories import categories
from modules.transactions import transactions

from .models import CategoryTotal


class ReportRepository(BaseRepository[CategoryTotal]):
    async def get_categories_totals(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> List[CategoryTotal]:
        transactions_with_categories = transactions.join(
            categories, categories.c.id == transactions.c.category_id, isouter=True
        )
        query = (
            select(
                [
                    json_object(categories).label('category'),
                    func.sum(transactions.c.outcome).label('total'),
                ]
            )
            .select_from(transactions_with_categories)
            .where(
                and_(
                    transactions.c.user_id == user_id,
                    transactions.c.at_date >= start_date,
                    transactions.c.at_date <= end_date,
                )
            )
            .group_by(categories.c.id)
            .order_by(literal_column('total').desc())
        )

        return await self._fetch_all(query)


reports_repo = ReportRepository(
    db=database,
    model_class=CategoryTotal,
)
