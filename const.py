from enum import Enum


class TransactionType(str, Enum):
    EXPENSE = 'expense'
    INCOME = 'income'


DEFAULT_ACCOUNT_NAME = 'Default'
