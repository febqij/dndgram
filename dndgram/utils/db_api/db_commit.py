from sqlalchemy.exc import IntegrityError

from utils.db_api.session import session
from utils.db_api.schemas.user import User

from data.config import logger


def commit(user: User):
    session.add(user)

    try:
        session.commit()
        logger.debug(f"Успешный коммит данных:\n{user.__str__()}")
        return True
    except IntegrityError as error:
        session.rollback()
        logger.debug(f"IntegrityError.orig: {error.orig}")
        logger.debug(f"IntegrityError.statement: {error.statement}")
        return False
