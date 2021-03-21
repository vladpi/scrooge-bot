import logging

from aiogram import executor
from aiogram.dispatcher import Dispatcher, filters

from bot import dispatcher, handlers
from bot.const import history_cb
from bot.middlewares import UserMiddleware
from bot.resources import buttons
from bot.states import AddExpense
from modules.db import database

logging.basicConfig(level=logging.INFO)


def register_handlers(dp: Dispatcher):
    # Main
    dp.register_message_handler(handlers.start, filters.CommandStart(), state='*')

    # Add Expense
    dp.register_message_handler(
        handlers.add_expense_entry, filters.Text(equals=buttons.ADD_EXPENSE),
    )
    dp.register_message_handler(
        handlers.add_expense_amount_and_comment, state=AddExpense.amount_and_comment,
    )
    dp.register_message_handler(handlers.add_expense_date, state=AddExpense.date)
    dp.register_message_handler(handlers.add_expense_category, state=AddExpense.category)

    # History
    dp.register_message_handler(handlers.history_entry, filters.Text(equals=buttons.HISTORY))
    dp.register_callback_query_handler(handlers.history_page, history_cb.filter())


def register_middlewares(dp: Dispatcher):
    dp.middleware.setup(UserMiddleware())


async def on_startup(dp: Dispatcher):
    register_handlers(dp)
    register_middlewares(dp)
    await database.connect()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_startup, skip_updates=True)
