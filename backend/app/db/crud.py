"""CRUD utils - Create, Read, Update, Delete
"""
# TODO do type ignore in mypy config, see https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-type-hints-for-third-party-library
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import select # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Optional, TypeVar, Union
from datetime import datetime
from . import models, schemas


ModelType = TypeVar("ModelType", bound=schemas.BaseModel)


async def update_object(obj: ModelType, obj_data: Dict[str, Any], update_data: Dict[str, Any]) -> None:
    for field in obj_data:
        if field in update_data:
            setattr(obj, field, update_data[field]) # does this happen inplace?
    return obj


async def create_workflow(session: AsyncSession, workflow: schemas.WorkflowCreate) -> models.Workflow:
    db_workflow = models.Workflow(**workflow.dict())
    session.add(db_workflow)
    await session.commit()
    await session.refresh(db_workflow)
    return db_workflow


async def read_workflow_multi(session: AsyncSession, offset: int=0, limit: int=100) -> List[models.Workflow]:
    result = await session.execute(
            select(models.Workflow).offset(offset).limit(limit)
        )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj_list: Optional[List[models.Workflow]] = result.scalars().all()
    return db_obj_list


async def update_workflow(session: AsyncSession, workflow: schemas.WorkflowUpdate) -> Union[models.Workflow, None]:
    """Update workflow and associated jobs

    The workflow update contains a Dict, msg.
    The kind of update must be inferred from the contents of msg.

    Args:
        session (AsyncSession): database session
        workflow (schemas.WorkflowUpdate): new data to update workflow with

    Returns:
        models.Workflow: updated workflow
    """
    query = await session.execute(
            select(models.Workflow).where(models.Workflow.id == workflow.id)
        )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj: Optional[models.Workflow] = query.scalars().first()
    obj_data = jsonable_encoder(db_obj)
    update_data = workflow.dict(exclude_unset=True)
    
    if workflow.msg["level"] == "job_info":
        pass
    elif workflow.msg["level"] == "progress":
        db_obj = await update_object(db_obj, obj_data, update_data["msg"])
        if db_obj.done == db_obj.total:
            setattr(db_obj, "completed_at", datetime.now())
            setattr(db_obj, "status", "Done")
    elif workflow.msg["level"] == "resources_info":
        # only used for actual runs
        pass
    elif workflow.msg["level"] == "debug":
        # infer start / done
        pass
    else:
        # TODO handle other cases
        pass
    
    # timestamp is always updated
    setattr(db_obj, "last_update_at", update_data["timestamp"]) # TODO rename to timestamp?
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    return db_obj