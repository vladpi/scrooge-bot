from typing import Any, Dict

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Body, Depends
from fastapi_security_telegram_webhook import OnlyTelegramNetwork
from starlette import status
from starlette.responses import Response

from .dependencies import get_bot_dispatcher

telegram_webhook_security = OnlyTelegramNetwork()
router = APIRouter(prefix='/tg')


@router.post('/webhook/{secret:str}', include_in_schema=False)
async def handle_webhook(
    secret: str,
    raw_update: Dict[str, Any] = Body(...),
    dp: Dispatcher = Depends(get_bot_dispatcher),
    security: OnlyTelegramNetwork = Depends(telegram_webhook_security),
) -> Response:
    telegram_update = Update(**raw_update)
    await dp.process_update(telegram_update)
    return Response(status_code=status.HTTP_200_OK)
