from datetime import date
from typing import List

from sqlalchemy import and_, func, literal_column, select

from libs.base_service import BaseDBService
from modules.transactions.tables import transactions

from .schemas import CategoryTotalSchema


class ReportService(BaseDBService):
    async def get_categories_totals(
        self, user_id: int, start_date: date, end_date: date,
    ) -> List[CategoryTotalSchema]:
        query = (
            select([
                transactions.c.category,
                func.sum(transactions.c.amount).label('total'),
            ])
            .where(
                and_(
                    transactions.c.user_id == user_id,
                    transactions.c.on_date >= start_date,
                    transactions.c.on_date <= end_date,
                )
            )
            .group_by(transactions.c.category)
            .order_by(literal_column('total').desc())
        )

        records = await self.db.fetch_all(query)

        return [CategoryTotalSchema.parse_obj(record) for record in records]


report_service = ReportService()
