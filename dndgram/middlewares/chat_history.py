from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.exceptions import TelegramBadRequest

from utils.db_api.schemas import User, Chat
import utils.db_api.db_quick_commands as dbqc
import utils.keyboards as kb

from data.config import logger

from bot import bot
import pprint as pp

async def init_chat_list(user: User):
    chat_list = [x for x in user.chat if len(user.chat) > 1]
    chat_list.sort(key=lambda x: x.message_id)
    return chat_list


async def message_cleaner(user: User, event_data: str):
    chat_list = await init_chat_list(user)
    if event_data == 'location:back':
        await bot.delete_message(
            chat_id=user.id,
            message_id=chat_list[-1].message_id
        )
        await dbqc.delete_chat_row(chat_list[-1])
        del chat_list[-1]
    for chat in chat_list[:-1]:
        try:
            await bot.delete_message(
                chat_id=user.id,
                message_id=chat.message_id
            )
            logger.debug("Сработало удаление bot.delete_message")
        except TelegramBadRequest as e:
            logger.warning(
                "Error deleting the message at ChatHistoryCallbackQueryMiddleware."
                " The message has probably already been deleted by the user."
                f" Details:\n{e.message}"
            )
        finally:
            await dbqc.delete_chat_row(chat)


class ChatHistoryCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if not await dbqc.select_message(event.message.message_id):
            await dbqc.insert_message_id(event.message)

        user = await dbqc.get_user_mesages(event.from_user.id)

        
        await message_cleaner(user[0], event.data)
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
