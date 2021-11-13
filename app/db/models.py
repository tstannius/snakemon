"""SQLAlchemy database models

These models define the database tables
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # TODO: consider making django-like table name
        # Alembic and FastAPI will still know what to do
        return cls.__name__.lower()


class Workflow(Base):
    id = Column(Integer, primary_key=True)
    workflow = Column(String(50), unique=False)
    name = Column(String(50), unique=False)
    status = Column(String(30), unique=False)
    done = Column(Integer, unique=False)
    total = Column(Integer, unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_update_at = Column(String(30)) # TODO: use proper DateTime

    def __init__(self, workflow, name, status=None):
        self.workflow = workflow
        self.name = name
        self.status = status
        self.done = 0
        self.total = 1
        self.started_at = datetime.now()
