from sqlalchemy import null

from aiogram import types
from aiogram.fsm.context import FSMContext

from sqlalchemy import delete, select, update
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
        user_id=message.chat.id,
        message_id=message.message_id
    )
    session.add(chat)
    if commit(chat):
        logger.debug(f"Добавлено в tables.chat:\n{chat.__str__()}")


async def delete_chat_row(chat: Chat):
    sql_command = delete(Chat).where(Chat.message_id == chat.message_id)
    session.execute(sql_command)
    if commit(chat):
        logger.debug(f"Удалена запись в tables.chat:\n{chat.__str__()}")


async def get_last_bot_message(user_id: int):
    """
    Returns the last record from DB containing the inline keyboard in the
    dialog with the user.
    """
    return (
        session.scalars(
            select(User).filter_by(id=user_id).options(joinedload(User.chat))
        ).unique().first()
    )


async def insert_age(message: types.Message):
    """Сохранение значение возраста в БД."""
    session.execute(
        update(User)
        .where(User.id == message.from_user.id)
        .values(age=message.text)
        .execution_options(synchronize_session="fetch")
    )
    session.commit()
    return message.text


async def delete_age(user: types.User):
    """Тоже самое, что и функция insert_age, но вставляет значение None."""
    try:
        session.execute(
            update(User)
            .where(User.id == user.id)
            .values(age=null())
            .execution_options(synchronize_session="fetch")
        )
        session.commit()
        return True
    except Exception as e:
        logger.error(
            f"shemas/db_quick_command.py at delete_age function:\n{e.__traceback__}"
        )
        return False


async def insert_gender(callbackquery: types.CallbackQuery):
    value = (callbackquery.data).split(":")[1]
    session.execute(
        update(User)
        .where(User.id == callbackquery.from_user.id)
        .values(gender=value)
        .execution_options(synchronize_session="fetch")
    )
    session.commit()
    return value


async def delete_gender(user: types.User):
    try:
        session.execute(
            update(User)
            .where(User.id == user.id)
            .values(gender=null())
            .execution_options(synchronize_session="fetch")
        )
        session.commit()
        return True
    except Exception as e:
        logger.error(
            f"shemas/db_quick_command.py at delete_gender function:\n{e.__traceback__}"
        )
        return False


async def get_preferences(user_id: int):
    return session.execute(
        select(User.preferences).filter_by(id=user_id)
    ).scalar_one()


async def insert_preference(preferences: str, user_id: int):
    try:
        session.execute(
            update(User)
            .where(User.id == user_id)
            .values(preferences=preferences)
            .execution_options(synchronize_session="fetch")
        )
        session.commit()
        return True
    except Exception as e:
        logger.error(
            f"shemas/db_quick_command.py at `insert_preference` function:\n{e.__traceback__}"
        )
        return False


async def delete_preference(preferences: str, user_id: int):
    """
    It's not really a deletion. When you click the button again, the cell in
    the table is simply overwritten with a new list, but without the specified
    value.
    """
    try:
        session.execute(
            update(User)
            .where(User.id == user_id)
            .values(preferences=preferences)
            .execution_options(synchronize_session="fetch")
        )
        session.commit()
        return True
    except Exception as e:
        logger.error(
            f"shemas/db_quick_command.py at `delete_preference` function:\n{e.__traceback__}"
        )
        return False


async def clear_preferences(user_id: int):
    """
    It is used if there should be no values left in the preference list after
    the user clicks the button.
    """
    try:
        session.execute(
            update(User)
            .where(User.id == user_id)
            .values(preferences=null())
            .execution_options(synchronize_session="fetch")
        )
        session.commit()
        return True
    except Exception as e:
        logger.error(
            f"shemas/db_quick_command.py at `clear_preferences` function:\n{e.__traceback__}"
        )
        return False
