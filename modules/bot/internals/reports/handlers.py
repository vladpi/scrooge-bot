import logging
from datetime import datetime
from typing import TYPE_CHECKING, Dict

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from modules.reports import ReportPeriod, get_report

from ...bot import dispatcher
from .. import buttons
from . import views
from .consts import reports_cb

if TYPE_CHECKING:
    from modules.users import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dispatcher.message_handler(filters.Text(equals=buttons.REPORTS))
async def reports_entry(message: types.Message, state: FSMContext, user: 'User'):
    report = await get_report(
        user.id,
        end_date=datetime.utcnow().date(),  # FIXME for localized date
        period=ReportPeriod.DAY,
    )
    await views.report(message.bot, user.id, report)


@dispatcher.callback_query_handler(reports_cb.filter())
async def report_for_period(
    query: types.CallbackQuery,
    callback_data: Dict[str, str],
    user: 'User',
):
    try:
        period = ReportPeriod(callback_data.get('period'))
    except ValueError:
        pass  # FIXME fallback message

    report = await get_report(
        user.id,
        end_date=datetime.utcnow().date(),
        period=period,  # FIXME for localized date
    )
    await views.report(query.bot, user.id, report, message_for_update=query.message)
