"""SQLAlchemy database models

These models define the database tables
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from datetime import datetime

from .database import Base


class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    workflow = Column(String(50), unique=False)
    name = Column(String(50), unique=False)
    status = Column(String(30), unique=False)
    done = Column(Integer, unique=False)
    total = Column(Integer, unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    def __init__(self, workflow, name, status=None):
        self.workflow = workflow
        self.name = name
        self.status = status
        self.done = 0
        self.total = 1
        self.started_at = datetime.now()
