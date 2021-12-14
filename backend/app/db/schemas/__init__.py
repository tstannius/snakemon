"""Pydantic schemas

Schemas aka. models. We use the term schemas here to not confuse schemas with
SQLAlchemy models.

Schemas are used by FastAPI for request validation, i.e. request contents and
typing.
"""
from .job import Job, JobCreate, JobUpdate
from .workflow import Workflow, WorkflowCreate, WorkflowUpdate
