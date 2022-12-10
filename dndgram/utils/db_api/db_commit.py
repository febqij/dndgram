from sqlalchemy.exc import IntegrityError

from utils.db_api.session import session

from data.config import logger


def commit(object):
    try:
        session.commit()
        return True
    except IntegrityError as error:
        session.rollback()
        logger.debug(
            f"IntegrityError.orig: {error.orig}"
            f"IntegrityError.statement: {error.statement}"
        )
        return False
