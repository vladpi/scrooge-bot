import logging
from datetime import date, datetime, timedelta
from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import views
from bot.resources import buttons
from schemas.expense import ExpenseSchema
from bot.states import AddExpense
from bot.utils import parsing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def add_expense_entry(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy.setdefault('expense', {})

    await views.add_expense.add_expense_amount(message.chat.id)
    await AddExpense.amount_and_comment.set()


async def add_expense_amount_and_comment(message: types.Message, state: FSMContext):
    amount, comment = parsing.parse_amount_and_comment(message.text)

    if amount is None:
        await views.add_expense.wrong_expense_amount(message.chat.id)

    else:
        async with state.proxy() as proxy:
            proxy['expense']['amount'] = amount
            proxy['expense']['comment'] = comment

        await views.add_expense.add_expense_date(message.chat.id)
        await AddExpense.date.set()


async def add_expense_date(message: types.Message, state: FSMContext):
    parsed_date: Optional[date]

    if message.text == buttons.TODAY:
        parsed_date = datetime.utcnow().date()  # FIXME localize date

    elif message.text == buttons.YESTERDAY:
        parsed_date = (datetime.utcnow() - timedelta(days=1)).date()  # FIXME localize date

    else:
        parsed_date = parsing.parse_date(message.text)

    if parsed_date is None:
        await views.add_expense.wrong_expense_date(message.chat.id)

    else:
        async with state.proxy() as proxy:
            proxy['expense']['on_date'] = parsed_date

        await views.add_expense.select_category(message.chat.id)
        await AddExpense.category.set()


async def add_expense_category(message: types.Message, state: FSMContext):
    category = message.text

    async with state.proxy() as proxy:
        proxy['expense']['category'] = category

        expense = ExpenseSchema(**proxy['expense'])

    await views.add_expense.expense_created(message.chat.id, expense)
    await state.finish()
