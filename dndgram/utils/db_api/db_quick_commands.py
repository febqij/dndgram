from aiogram import types
from aiogram.fsm.context import FSMContext

from sqlalchemy import delete
from sqlalchemy.orm import joinedload

from utils.db_api.session import session
from utils.db_api.schemas import User, Chat
from utils.db_api.db_commit import commit
from data.config import logger


async def register_user(message: types.Message):
    username = message.from_user.username or None
    user = User(
        id=message.from_user.id,
        username=username,
    )
    session.add(user)
    if commit(user):
        logger.debug(f"Успешный add-коммит данных:\n{user.__str__()}")


async def select_user(user_id):
    """Return user data from Postgres."""
    return session.query(User).filter(User.id == user_id).first()


async def select_message(message_id):
    """Return message data from Postgres for current chat."""
    return session.query(Chat).filter(Chat.message_id == message_id).first()


async def get_user_mesages(user_id):
    """Return all user messages Postgres for current bot."""
    return session.query(User).options(joinedload('chat')).filter(User.id == user_id).all()


async def insert_message_id(message: types.Message):
    chat = Chat(
        user_id = message.chat.id,
        message_id = message.message_id
    )
    session.add(chat)
    if commit(chat):
        logger.debug(f"Добавлено в tables.chat:\n{chat.__str__()}")

async def delete_chat_row(chat: Chat):
    sql_command = delete(Chat).where(Chat.message_id == chat.message_id)
    session.execute(sql_command)
    if commit(chat):
        logger.debug(f"Удалена запись в tables.chat:\n{chat.__str__()}")
