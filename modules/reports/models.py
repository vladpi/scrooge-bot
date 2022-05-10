from datetime import date
from decimal import Decimal
from typing import List

from libs.base_model import BaseModel
from modules.categories import Category

from .consts import ReportPeriod


class CategoryTotal(BaseModel):
    category: Category
    total: Decimal


class Report(BaseModel):
    period: ReportPeriod
    period_start: date
    period_end: date
    categories_totals: List[CategoryTotal]
