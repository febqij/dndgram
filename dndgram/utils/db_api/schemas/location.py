from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.orm import relationship

from utils.db_api.session import Base


class Location(Base):
    """
    To get users in the current location: <LocationObject>.users
    """
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    city = Column(VARCHAR(length=255), nullable=True)
    state = Column(VARCHAR(length=255), nullable=True)
    users = relationship('User', back_populates="location")
