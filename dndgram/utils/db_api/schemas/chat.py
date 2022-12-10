from sqlalchemy import (
    Column, Integer, String, VARCHAR, SmallInteger, TEXT, ForeignKey
)
from sqlalchemy.orm import relationship

from utils.db_api.session import Base


class Chat(Base):
    """
    Содержит в себе информацию об id всех сообщений в диалоге с пользователем.
    """
    __tablename__ = 'chat'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates="chat")
    message_id = Column(Integer,  primary_key=True)

    def __str__(self):
        return {
            "message_id": self.message_id,
            "user_id": self.user_id
        }
