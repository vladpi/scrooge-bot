from aiogram.dispatcher.filters.state import State, StatesGroup


class AddExpense(StatesGroup):
    account = State()
    amount_and_comment = State()
    date = State()
    category = State()
