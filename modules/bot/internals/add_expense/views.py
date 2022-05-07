from typing import TYPE_CHECKING, List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from .. import buttons
from ..main.views import main_menu

if TYPE_CHECKING:
    from aiogram import Bot

    from modules.accounts import Account
    from modules.transactions import Transaction


async def select_account(bot: 'Bot', to_chat_id: int, accounts: List['Account']):
    keyboard = [[KeyboardButton(account.name)] for account in accounts]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери счет',
        reply_markup=reply_markup,
    )


async def add_expense_amount(bot: 'Bot', to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text='Отправь сумму и комментарий',
        reply_markup=reply_markup,
    )


async def wrong_expense_amount(bot: 'Bot', to_chat_id: int):
    reply_markup = ReplyKeyboardRemove()
    await bot.send_message(
        chat_id=to_chat_id,
        text='Не вижу сумму.\nПовтори в формате: <pre>123.45</pre>',
        reply_markup=reply_markup,
    )


async def add_expense_date(bot: 'Bot', to_chat_id: int):
    keyboard = [
        [KeyboardButton(buttons.YESTERDAY), KeyboardButton(buttons.TODAY)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери или отправь дату',
        reply_markup=reply_markup,
    )


async def wrong_expense_date(bot: 'Bot', to_chat_id: int):
    await bot.send_message(
        chat_id=to_chat_id,
        text='Не вижу даты.\nПовтори в формате: <pre>01.02.20</pre>',
    )


async def select_category(bot: 'Bot', to_chat_id: int, categories: List[str]):
    keyboard = [[KeyboardButton(category)] for category in categories]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(
        chat_id=to_chat_id,
        text='Выбери категорию',
        reply_markup=reply_markup,
    )


async def expense_created(bot: 'Bot', to_chat_id: int, expense: 'Transaction'):
    text = f'Расход создан!\n\n{str(expense)}'
    await main_menu(bot, to_chat_id, text=text)
