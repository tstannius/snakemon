from fastapi import Form
from typing import Any, Dict, List, Optional, Type
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Json
import inspect


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    
    Background:
    https://github.com/tiangolo/fastapi/issues/1989
    https://github.com/tiangolo/fastapi/issues/2387
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


class WorkflowBase(BaseModel):
    pass


class WorkflowCreate(WorkflowBase):
    workflow: str    # workflow type
    name: str        # name of run


class WorkflowMetadata(WorkflowBase):
    snakefile: Path
    command: str
    workdir: Path


@as_form
class WorkflowMessage(WorkflowBase):
    level: str
    msg: Optional[str] = None
    done: Optional[int] = None
    total: Optional[int] = None
    # resources
    # _cores: Optional[int] = None # nested in msg
    # _nodes: Optional[int] = None # nested in msg
    # jobinfo
    jobid: Optional[int] = None
    name: Optional[str] = None
    local: Optional[bool] = None
    input: Optional[List[str]] = None # TODO use path type
    output: Optional[List[str]] = None
    log: Optional[List[str]] = None
    benchmark: Optional[str] = None
    wildcards: Optional[Dict[str, Any]]
    # reason
    # resources # include and interpret
    # priority
    # threads
    # indent
    # is_checkpoint
    # printshellcmd
    # is_handover


@as_form
class WorkflowUpdate(WorkflowBase):
    id: int
    # msg: Json[WorkflowMessage] # TODO: consider WorkflowMessage, currently no advantage since not in docs
    msg: Json[Dict[str, Any]] # type: ignore TODO: find out why mypy doesn't like Json
    timestamp: str


class Workflow(WorkflowCreate):
    id: int          # primary key
    status: Optional[str] # TODO: for all optionals, consider an init value in models.py
    done: Optional[int] # TODO: is init, so should never be None, but is when pipeline running?
    total: Optional[int] # TODO: is init, so should never be None, but is when pipeline running?
    started_at: datetime
    completed_at: Optional[datetime]
    last_update_at: Optional[datetime]
    timestamp: str

    class Config:
        orm_mode = True
