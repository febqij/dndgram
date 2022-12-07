from sqlalchemy import Column, ForeignKey, Integer, BOOLEAN
from sqlalchemy.orm import relationship

from utils.db_api.session import Base


class Player(Base):
    __tablename__ = 'player'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates="is_player")
    experience = (BOOLEAN)
