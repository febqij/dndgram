from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker


load_dotenv()


class Config(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: SecretStr
    DATABASE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()

engine = create_engine(
    f"postgresql+psycopg2://{config.USER}:{config.PASSWORD}@{config.HOST}/{config.DATABASE}"
)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()
