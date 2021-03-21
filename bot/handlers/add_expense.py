import logging
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from bot import dispatcher, views
from bot.resources import buttons
from bot.states import AddExpense
from bot.utils import parsing
from modules.accounts import get_user_accounts
from modules.transactions import create_expense_transaction

if TYPE_CHECKING:
    from modules.users import UserSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dispatcher.message_handler(filters.Text(equals=buttons.ADD_EXPENSE))
async def add_expense_entry(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy.setdefault('expense', {})

    await views.add_expense.add_expense_amount(message.chat.id)
    await AddExpense.amount_and_comment.set()


@dispatcher.message_handler(state=AddExpense.amount_and_comment)
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


@dispatcher.message_handler(state=AddExpense.date)
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


@dispatcher.message_handler(state=AddExpense.category)
async def add_expense_category(message: types.Message, state: FSMContext, user: 'UserSchema'):
    category = message.text

    async with state.proxy() as proxy:
        proxy['expense']['category'] = category

        account = (await get_user_accounts(user.id))[0]  # FIXME select account step

        expense = await create_expense_transaction(
            user_id=user.id,
            account_id=account.id,
            **proxy.pop('expense'),
        )

    await views.add_expense.expense_created(message.chat.id, expense)
    await state.finish()
