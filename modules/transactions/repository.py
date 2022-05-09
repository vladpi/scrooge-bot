from asyncio import gather
from datetime import date
from typing import List, Optional, Tuple

import sqlalchemy as sa
from sqlalchemy import func, select

from app import database
from libs.base_repo import BaseModelRepository
from libs.sql_utils import json_object, json_object_or_none
from modules.accounts import accounts
from modules.categories import categories

from .models import Transaction
from .tables import transactions


class TransactionRepository(BaseModelRepository[Transaction]):
    @property
    def select_query(self) -> sa.sql.Select:
        outcome_accounts = accounts.alias('outcome_account')
        income_accounts = accounts.alias('income_accounts')
        transactions_with_linked = (
            self.table.join(categories, categories.c.id == self.table.c.category_id, isouter=True)
            .join(
                outcome_accounts,
                outcome_accounts.c.id == self.table.c.outcome_account_id,
                isouter=True,
            )
            .join(
                income_accounts,
                income_accounts.c.id == self.table.c.income_account_id,
                isouter=True,
            )
        )
        return sa.select(
            [
                self.table,
                json_object(categories).label('category'),
                json_object_or_none(outcome_accounts).label('outcome_account'),
                json_object_or_none(income_accounts).label('income_account'),
            ]
        ).select_from(transactions_with_linked)

    async def get_for_user(
        self,
        user_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        at_date: Optional[date] = None,
    ) -> List['Transaction']:
        query = (
            self.select_query
            .where(transactions.c.user_id == user_id)
            .order_by(
                transactions.c.at_date.desc(),
                transactions.c.created_at.desc(),
            )
        )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        if at_date is not None:
            query = query.where(transactions.c.at_date == at_date)

        return await self._fetch_all(query)

    async def count_for_user(self, user_id: int) -> int:
        query = (
            select([transactions])
            .where(transactions.c.user_id == user_id)
            .with_only_columns([func.count()])
        )
        return await self.db.execute(query)

    async def get_dates_for_user(
        self,
        user_id: int,
        current_date: Optional[date] = None,
    ) -> Tuple[Optional[date], Optional[date], Optional[date]]:
        if current_date is None:
            query = select([func.max(transactions.c.at_date)]).where(
                transactions.c.user_id == user_id
            )
            current_date = await self.db.fetch_val(query)

        if current_date is None:
            return None, None, None

        prev_query = select([func.max(transactions.c.at_date)]).where(
            sa.and_(
                transactions.c.user_id == user_id,
                transactions.c.at_date < current_date,
            ),
        )
        next_query = select([func.min(transactions.c.at_date)]).where(
            sa.and_(
                transactions.c.user_id == user_id,
                transactions.c.at_date > current_date,
            )
        )

        prev_date, next_date = await gather(
            self.db.fetch_val(prev_query), self.db.fetch_val(next_query)
        )

        return prev_date, current_date, next_date


transactions_repo = TransactionRepository(
    db=database,
    model_class=Transaction,
    table=transactions,
    pk_field=transactions.c.id,
)
