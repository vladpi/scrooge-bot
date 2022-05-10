from typing import TYPE_CHECKING, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from modules.reports import ReportPeriod

from .consts import reports_cb

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message

    from modules.reports import Report


async def report(
    bot: 'Bot',
    to_chat_id: int,
    report: 'Report',
    message_for_update: Optional['Message'] = None,
):
    if report.period == ReportPeriod.DAY:
        message = f'<b>{report.period_start:%d.%m.%Y}</b>\n\n'
    else:
        message = f'<b>{report.period_start:%d.%m.%Y} - {report.period_end:%d.%m.%Y}</b>\n\n'

    for category_total in report.categories_totals:
        message += f'<b>{category_total.category.name}:</b> {category_total.total}\n'

    day_period_button = InlineKeyboardButton(
        'За день', callback_data=reports_cb.new(period=ReportPeriod.DAY)
    )
    week_period_button = InlineKeyboardButton(
        'За неделю', callback_data=reports_cb.new(period=ReportPeriod.WEEK)
    )
    month_period_button = InlineKeyboardButton(
        'За месяц', callback_data=reports_cb.new(period=ReportPeriod.MONTH)
    )

    reply_markup = InlineKeyboardMarkup(row_width=1)
    if report.period == ReportPeriod.DAY:
        reply_markup.add(
            week_period_button,
            month_period_button,
        )
    elif report.period == ReportPeriod.WEEK:
        reply_markup.add(
            day_period_button,
            month_period_button,
        )
    elif report.period == ReportPeriod.MONTH:
        reply_markup.add(
            day_period_button,
            week_period_button,
        )

    if message_for_update is not None:
        await message_for_update.edit_text(text=message, reply_markup=reply_markup)

    else:
        await bot.send_message(chat_id=to_chat_id, text=message, reply_markup=reply_markup)
