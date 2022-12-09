from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from utils.db_api.db_quick_commands import insert_message_id, select_message

from data.config import logger


class ChatHistoryMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if not await select_message(event.message.message_id):
            await insert_message_id(event.message)

        from handlers import router_profile
        return await handler(event, data)
