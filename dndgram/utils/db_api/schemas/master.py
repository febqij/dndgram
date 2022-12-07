from sqlalchemy import Column, ForeignKey, Integer, BOOLEAN
from sqlalchemy.orm import relationship

from utils.db_api.session import Base


class Master(Base):
    __tablename__ = 'master'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates="is_master")
    experience = (BOOLEAN)
