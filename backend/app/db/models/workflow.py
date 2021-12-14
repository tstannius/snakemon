from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Workflow(Base):
    id = Column(Integer, primary_key=True)
    workflow = Column(String(50), unique=False)
    name = Column(String(50), unique=False)
    status = Column(String(30), unique=False)
    done = Column(Integer, unique=False)
    total = Column(Integer, unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_update_at = Column(DateTime)
    timestamp = Column(String(30))
    
    jobs = relationship("Job", back_populates="workflow") # type: ignore

    def __init__(self, workflow, name):
        self.workflow = workflow
        self.name = name
        self.done = 0
        self.total = 0
        self.started_at = datetime.now()
        self.last_update_at = datetime.now()
