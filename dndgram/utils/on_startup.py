from utils.db_api.session import Base, engine

from data.config import logger

from bot import dp


@dp.startup()
async def on_startup_chemas_create():
    """Импортируем все модели для БД перед созданием схем."""
    try:
        import utils.db_api.schemas
        Base.metadata.create_all(bind=engine)
        logger.info("Schemas on startup was updated.")
    except Exception as error:
        logger.exception(f"on_startup_notify error:\n{error}")
