from sqlalchemy.exc import IntegrityError

from utils.db_api.session import session

from data.config import logger


def commit(row):
    session.add(row)

    try:
        session.commit()
        logger.debug(f"Успешный коммит данных:\n{row.__str__()}")
        return True
    except IntegrityError as error:
        session.rollback()
        logger.debug(
            f"IntegrityError.orig: {error.orig}"
            f"IntegrityError.statement: {error.statement}"
        )
        return False
