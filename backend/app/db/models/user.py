from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String(64), unique=True, nullable=False)
        username = Column(String(32), unique=True, index=True, nullable=False)
        hashed_password = Column(String(128), nullable=False)
