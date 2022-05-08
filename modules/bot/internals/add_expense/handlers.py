import logging
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from modules.accounts import get_user_account_by_name, get_user_accounts
from modules.categories import get_user_categories, get_user_category_by_name
from modules.transactions import create_outcome_transaction

from ...bot import dispatcher
from .. import buttons, parsing
from . import views
from .states import AddExpense

if TYPE_CHECKING:
    from modules.users import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dispatcher.message_handler(filters.Text(equals=buttons.ADD_EXPENSE))
async def add_expense_entry(message: types.Message, state: FSMContext, user: 'User'):
    async with state.proxy() as proxy:
        proxy.setdefault('expense', {})

    await views.add_expense_amount(message.bot, message.chat.id)
    await AddExpense.amount_and_comment.set()


@dispatcher.message_handler(state=AddExpense.amount_and_comment)
async def add_expense_amount_and_comment(
    message: types.Message,
    state: FSMContext,
    user: 'User',
):
    amount, comment = parsing.parse_amount_and_comment(message.text)

    if amount is None:
        await views.wrong_expense_amount(message.bot, message.chat.id)
        return

    async with state.proxy() as proxy:
        proxy['expense']['amount'] = amount
        proxy['expense']['comment'] = comment

    accounts = await get_user_accounts(user.id)
    if len(accounts) > 1:
        await views.select_account(message.bot, message.chat.id, accounts)
        await AddExpense.account.set()

    else:
        async with state.proxy() as proxy:
            proxy['expense']['account_id'] = accounts[0].id
            proxy['expense']['currency'] = accounts[0].currency

        await views.add_expense_date(message.bot, message.chat.id)
        await AddExpense.date.set()


@dispatcher.message_handler(state=AddExpense.account)
async def add_expense_account(message: types.Message, state: FSMContext, user: 'User'):
    account = await get_user_account_by_name(user.id, message.text)

    if account is None:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy['expense']['account_id'] = account.id
        proxy['expense']['currency'] = account.currency

    await views.add_expense_date(message.bot, message.chat.id)
    await AddExpense.date.set()


@dispatcher.message_handler(state=AddExpense.date)
async def add_expense_date(message: types.Message, state: FSMContext, user: 'User'):
    parsed_date: Optional[date]

    if message.text == buttons.TODAY:
        parsed_date = datetime.utcnow().date()  # FIXME localize date

    elif message.text == buttons.YESTERDAY:
        parsed_date = (datetime.utcnow() - timedelta(days=1)).date()  # FIXME localize date

    else:
        parsed_date = parsing.parse_date(message.text)

    if parsed_date is None:
        await views.wrong_expense_date(message.bot, message.chat.id)

    else:
        async with state.proxy() as proxy:
            proxy['expense']['at_date'] = parsed_date.strftime('%d.%m.%Y')

        categories = await get_user_categories(user.id)
        await views.select_category(message.bot, message.chat.id, categories)
        await AddExpense.category.set()


@dispatcher.message_handler(state=AddExpense.category)
async def add_expense_category(message: types.Message, state: FSMContext, user: 'User'):
    category = await get_user_category_by_name(user.id, message.text)

    if category is None:
        return  # FIXME message

    async with state.proxy() as proxy:
        proxy['expense']['category_id'] = category.id

        expense = await create_outcome_transaction(user_id=user.id, **proxy.pop('expense'))

    await views.expense_created(message.bot, message.chat.id, expense)
    await state.finish()
