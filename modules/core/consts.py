from enum import Enum


class Currency(str, Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'
