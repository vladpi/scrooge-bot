from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from modules.reports import ReportPeriod, ReportSchema

from ..bot import bot
from ..const import reports_cb


async def report(
    to_chat_id: int,
    report: ReportSchema,
    message_for_update: Optional[Message] = None,
):
    if report.period == ReportPeriod.DAY:
        message = f'<b>{report.period_start:%d.%m.%Y}</b>\n\n'
    else:
        message = f'<b>{report.period_start:%d.%m.%Y} - {report.period_end:%d.%m.%Y}</b>\n\n'

    for category_total in report.categories_totals:
        message += f'<b>{category_total.category}:</b> {category_total.total}\n'

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
