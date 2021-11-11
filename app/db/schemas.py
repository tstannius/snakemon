"""Pydantic schemas

Schemas aka. models. We use the term schemas here to not confuse schemas with
SQLAlchemy models

Schemas are used by FastAPI for request validation.
"""
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


class WorkflowBase(BaseModel):
    pass


class WorkflowCreate(WorkflowBase):
    workflow: str    # workflow type
    name: str        # name of run


class WorkflowMetadata(WorkflowBase):
    snakefile: Path
    command: str
    workdir: Path


class WorkflowUpdate(WorkflowBase):
    id: int
    timestamp: str
    msg: str


class Workflow(WorkflowCreate):
    id: int          # primary key
    status: str
    done: int
    total: int
    started_at: datetime
    completed_at: datetime
    last_update_at: datetime

    class Config:
        orm_mode = True
