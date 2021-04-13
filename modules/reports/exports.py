from datetime import date, timedelta
from typing import Optional

from .consts import ReportPeriod
from .schemas import ReportSchema
from .service import report_service


# FIXME for pagination
async def get_report(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    period: Optional[ReportPeriod] = ReportPeriod.DAY,
):
    delta = None
    if period == ReportPeriod.DAY:
        delta = timedelta(days=0)
    elif period == ReportPeriod.WEEK:
        delta = timedelta(days=6)
    elif period == ReportPeriod.MONTH:
        # FIXME for true month duration
        # _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
        delta = timedelta(days=30)

    if delta is None:
        raise ValueError(f'Bad period value: {period}')  # FIXME for custom error

    if start_date is not None:
        end_date = start_date + delta
    elif end_date is not None:
        start_date = end_date - delta
    else:
        raise ValueError('Cannot get report without dates')  # FIXME for custom error

    categories_totals = await report_service.get_categories_totals(user_id, start_date, end_date)

    return ReportSchema(
        period=period,
        period_start=start_date,
        period_end=end_date,
        categories_totals=categories_totals,
    )
