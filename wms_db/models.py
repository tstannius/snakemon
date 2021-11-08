"""SQLAlchemy database models

These models define the database tables
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")



class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    workflow = Column(String(50), unique=False)
    workflow_id = Column(String(50), unique=True)
    name = Column(String(50), unique=False)
    status = Column(String(30), unique=False)
    done = Column(Integer, unique=False)
    total = Column(Integer, unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # def __init__(self, name=None, status=None):
    #     self.name = name
    #     self.status = status
    #     self.done = 0
    #     self.total = 1
    #     self.started_at = datetime.now()
