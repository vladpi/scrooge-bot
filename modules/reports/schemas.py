from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from .consts import ReportPeriod


class CategoryTotalSchema(BaseModel):
    category: str
    total: Decimal


class ReportSchema(BaseModel):
    period: ReportPeriod
    period_start: date
    period_end: date
    categories_totals: List[CategoryTotalSchema]
