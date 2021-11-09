"""Pydantic schemas

Schemas aka. models. We use the term schemas here to not confuse schemas with
SQLAlchemy models

Schemas are used by FastAPI for request validation.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class WorkflowBase(BaseModel):
    workflow: str    # workflow type
    name: str        # name of run


class WorkflowCreate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: int          # primary key
    status: str
    done: int
    total: int
    started_at: datetime
    completed_at: datetime

    class Config:
        orm_mode = True
