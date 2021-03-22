from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot import bot
from bot.const import CATEGORIES
from bot.resources import buttons, messages
from modules.accounts import AccountSchema
from modules.transactions import TransactionSchema

from .main import main_menu


async def select_account(to_chat_id: int, accounts: List[AccountSchema]):
    keyboard = [[KeyboardButton(account.name)] for account in accounts]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.SELECT_ACCOUNT,
        reply_markup=reply_markup,
    )


async def add_expense_amount(to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.ADD_EXPENSE_AMOUNT,
        reply_markup=reply_markup,
    )


async def wrong_expense_amount(to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.WRONG_EXPENSE_AMOUNT,
        reply_markup=reply_markup,
    )


async def add_expense_date(to_chat_id: int):
    keyboard = [
        [KeyboardButton(buttons.TODAY), KeyboardButton(buttons.YESTERDAY)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.SET_EXPENSE_DATE,
        reply_markup=reply_markup,
    )


async def wrong_expense_date(to_chat_id: int):
    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.WRONG_EXPENSE_AMOUNT,
    )


async def select_category(to_chat_id: int):
    keyboard = [[KeyboardButton(category)] for category in CATEGORIES]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text=messages.SELECT_CATEGORY,
        reply_markup=reply_markup,
    )


async def expense_created(to_chat_id: int, expense: TransactionSchema):
    text = messages.EXPENSE_CREATED.format(expense_card=str(expense))
    await main_menu(to_chat_id, text=text)
