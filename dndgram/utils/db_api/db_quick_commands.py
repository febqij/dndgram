from aiogram import types
from aiogram.fsm.context import FSMContext

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
    commit(user)


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
    commit(chat)


async def delete_chat_row(chat):
    session.delete(chat)
    session.commit()
    logger.debug("Успешное удаление записи:")
