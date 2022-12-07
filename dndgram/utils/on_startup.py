from utils.db_api.session import Base, engine

from data.config import logger


def on_startup_notify():
    try:
        import utils.db_api.schemas
        Base.metadata.create_all(bind=engine)
        logger.info(f"Schemas on was {Base.__str__} updated.")
    except Exception as error:
        logger.exception(f"on_startup_notify error:\n{error}")
