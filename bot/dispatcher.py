from aiogram import Dispatcher
from aiogram.dispatcher import filters

from . import handlers
from .bot import bot
from .resources import buttons
from .states import AddExpense
from .storage import storage

dispatcher = Dispatcher(bot, storage=storage)


def register_handlers(dp: Dispatcher):
    # Main
    dp.register_message_handler(handlers.start, filters.CommandStart(), state='*')

    # Add Expense
    dp.register_message_handler(handlers.add_expense_entry, filters.Text(equals=buttons.ADD_EXPENSE))
    dp.register_message_handler(handlers.add_expense_amount_and_comment, state=AddExpense.amount_and_comment)
    dp.register_message_handler(handlers.add_expense_date, state=AddExpense.date)
    dp.register_message_handler(handlers.add_expense_category, state=AddExpense.category)
