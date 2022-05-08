from datetime import date
from typing import List

from sqlalchemy import and_, func, literal_column, select

from app import database
from libs.base_repo import BaseRepository
from modules.transactions.tables import transactions

from .models import CategoryTotal


class ReportRepository(BaseRepository[CategoryTotal]):
    async def get_categories_totals(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> List[CategoryTotal]:
        query = (
            select(
                [
                    transactions.c.category_id,
                    func.sum(transactions.c.outcome).label('total'),
                ]
            )
            .where(
                and_(
                    transactions.c.user_id == user_id,
                    transactions.c.at_date >= start_date,
                    transactions.c.at_date <= end_date,
                )
            )
            .group_by(transactions.c.category_id)
            .order_by(literal_column('total').desc())
        )

        return await self._fetch_all(query)


reports_repo = ReportRepository(
    db=database,
    model_class=CategoryTotal,
)
