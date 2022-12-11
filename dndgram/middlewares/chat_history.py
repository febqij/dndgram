from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, BotCommand
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
                "Error deleting the message at ChatHistoryCallbackQueryMiddleware."
                " The message has probably already been deleted by the user."
                f" Details:\n{e.message}"
            )
        finally:
            await delete_chat_row(chat)


class ChatHistoryCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if not await select_message(event.message.message_id):
            await insert_message_id(event.message)

        user = await get_user_mesages(event.from_user.id)

        await message_cleaner(user[0])

        return await handler(event, data)


class ChatHistoryMessageMiddleware(BaseMiddleware):
    """Auto-delete all messages sent by users to keep the chat clean."""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        try:
            await bot.delete_message(
                chat_id=event.from_user.id,
                message_id=event.message_id
            )
        except TelegramBadRequest as e:
            logger.warning(
                "Error deleting the message at ChatHistoryMessageMiddleware. "
                "The message has probably already been deleted by the user. "
                f"Details:\n{e.message}"
            )

        return await handler(event, data)
