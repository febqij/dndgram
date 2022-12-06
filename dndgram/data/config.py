import os
import logging

from dotenv import load_dotenv

from pydantic import BaseSettings, SecretStr

load_dotenv()

logging.basicConfig(
    format='\n--- ---> %(asctime)s - %(name)s - %(levelname)s:\n%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    admins_id: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
