from enum import Enum


class ReportPeriod(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
