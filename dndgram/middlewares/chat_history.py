from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from utils.db_api.schemas import User, Chat
from utils.db_api.db_quick_commands import (
    insert_message_id, select_message, get_user_mesages, delete_chat_row
)

from data.config import logger

from bot import bot


async def message_cleaner(user: User):
    chat_list = [x for x in user.chat if len(user.chat) > 1]
    chat_list.sort(key=lambda x: x.message_id)

    for chat in chat_list[:-1]:
        try:
            await bot.delete_message(
                chat_id=user.id,
                message_id=chat.message_id
            )
        except TelegramBadRequest as e:
            logger.warning(
                "Error deleting the message. The message has probably already been "
                f"deleted by the user. Details:\n{e.message}"
            )
        finally:
            await delete_chat_row(chat)


class ChatHistoryMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if not await select_message(event.message.message_id):
            await insert_message_id(event.message)

        user = await get_user_mesages(event.from_user.id)

        await message_cleaner(user[0])

        from handlers import router_profile
        return await handler(event, data)
