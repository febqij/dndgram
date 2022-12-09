from sqlalchemy import (
    Column, Integer, String, VARCHAR, SmallInteger, TEXT, ForeignKey
)
from sqlalchemy.orm import relationship

from utils.db_api.session import Base


class User(Base):
    """To get the locations of a specific user: <UserObject>.location"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(length=255), nullable=True)
    gender = Column(String, nullable=True)
    age = Column(SmallInteger, nullable=True)
    preferences = Column(VARCHAR(length=255), nullable=True)
    bio = Column(TEXT, nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    location = relationship('Location', back_populates="users")
    is_master = relationship('Master', back_populates="user")
    is_player = relationship('Player', back_populates="user")
    chat = relationship('Chat', back_populates="user")

    def __str__(self):
        return {
            "id": self.id,
            "username": self.username,
            "gender": self.gender,
            "age": self.age,
            "preferences": self.preferences,
            "bio": self.bio,
            "location_id": self.location_id,
            "location": self.location,
            "is_master": self.is_master,
            "is_player": self.is_player
        }
