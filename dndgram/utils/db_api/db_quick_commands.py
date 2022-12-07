from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api.session import session
from utils.db_api.schemas.user import User
from utils.db_api.db_commit import commit
from data.config import logger


def register_user(message: types.Message):
    username = message.from_user.username or None
    user = User(
        id=message.from_user.id,
        username=username,
    )
    commit(user)


def select_user(user_id):
    """Return user data from Postgres."""
    return session.query(User).filter(User.id == user_id).first()
