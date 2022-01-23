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


ModelType = TypeVar("ModelType", bound=models.Base)


async def update_object(obj: ModelType, obj_data: Dict[str, Any], update_data: Dict[str, Any]) -> ModelType:
    """Update database object utility function

    Args:
        obj (ModelType): Object to update
        obj_data (Dict[str, Any]): obj as dict
        update_data (Dict[str, Any]): New data to use in update

    Returns:
        ModelType: Updated object
    """
    for field in obj_data:
        if field in update_data:
            setattr(obj, field, update_data[field]) # does this happen inplace?
    return obj



async def create_job(session: AsyncSession, job: schemas.JobCreate) -> models.Job:
    """Create workflow job

    Args:
        session (AsyncSession): Database session
        job (schemas.JobCreate): Schema of data to load into database

    Returns:
        models.Job: Database model object
    """
    db_job = models.Job(**job.dict())
    session.add(db_job)
    await session.commit()
    await session.refresh(db_job)
    return db_job



async def update_job(session: AsyncSession, job: schemas.JobUpdate) -> models.Job:
    """Update workflow job

    Args:
        session (AsyncSession): Database session
        job (schemas.JobUpdate): Schema of updated data to apply in database

    Returns:
        models.Job: Updated database model object
    """
    query = await session.execute(
            select(models.Job)
                .where(models.Job.workflow_id == job.workflow_id)
                .where(models.Job.jobid == job.jobid)
        )
    db_obj: Optional[models.Job] = query.scalars().first()
    obj_data = jsonable_encoder(db_obj)
    update_data = job.dict(exclude_unset=True)
    
    db_obj = await update_object(db_obj, obj_data, update_data)

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    return db_obj



async def create_workflow(session: AsyncSession, workflow: schemas.WorkflowCreate) -> models.Workflow:
    """Create workflow

    Args:
        session (AsyncSession): Database session
        workflow (schemas.WorkflowCreate): Schema of workflow to create

    Returns:
        models.Workflow: Created database model object
    """
    db_workflow = models.Workflow(**workflow.dict())
    session.add(db_workflow)
    await session.commit()
    await session.refresh(db_workflow)
    return db_workflow



async def read_workflow_single(session: AsyncSession, workflow_id: int) -> models.Workflow:
    """Read single workflow from database

    Args:
        session (AsyncSession): Database session
        workflow_id (int): Primary key of workflow

    Returns:
        models.Workflow: Workflow entry in database, if exists, or None
    """
    query = await session.execute(
            select(models.Workflow)
                .where(models.Workflow.id == workflow_id)
        )
    db_obj: Optional[models.Workflow] = query.scalars().first()
    return db_obj



async def read_workflow_multi(session: AsyncSession, offset: Optional[int]=0, limit: Optional[int]=100) -> List[models.Workflow]:
    """Read multiple workflows from database

    Args:
        session (AsyncSession): Database session
        offset (Optional[int], optional): Offset into database rows. Defaults to 0.
        limit (Optional[int], optional): Limit number of workflows returned. Defaults to 100.

    Returns:
        List[models.Workflow]: List of workflow entries in database
    """
    # TODO: Optional order_by
    result = await session.execute(
            select(models.Workflow).order_by(models.Workflow.id.desc()).offset(offset).limit(limit)
        )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj_list: Optional[List[models.Workflow]] = result.scalars().all()
    return db_obj_list



async def update_workflow(session: AsyncSession, workflow: schemas.WorkflowUpdate) -> Union[models.Workflow, None]:
    """Update workflow and associated jobs

    The workflow update contains a Dict, msg.
    The kind of update must be inferred from the contents of msg.

    Args:
        session (AsyncSession): Database session
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
        await create_job(session=session, job=schemas.JobCreate(**{"workflow_id": workflow.id, **workflow.msg}))
    elif workflow.msg["level"] == "progress":
        db_obj = await update_object(db_obj, obj_data, update_data["msg"])
        setattr(db_obj, "status", "Running")
        if db_obj.done == db_obj.total:
            setattr(db_obj, "completed_at", datetime.now())
            setattr(db_obj, "status", "Done")
    elif workflow.msg["level"] == "job_finished":
        await update_job(session, job=schemas.JobUpdate(**{"jobid": workflow.msg["jobid"],
                                                           "workflow_id": workflow.id, 
                                                           "completed_at": datetime.now(),
                                                           "status": "Done"}))
    elif workflow.msg["level"] == "job_error":
        await update_job(session, job=schemas.JobUpdate(**{"jobid": workflow.msg["jobid"],
                                                           "workflow_id": workflow.id, 
                                                           "status": "Error"}))
    elif workflow.msg["level"] == "resources_info":
        # only used for actual runs
        pass
    elif workflow.msg["level"] == "debug":
        # infer start / done
        pass
    elif workflow.msg["level"] == "error":
        setattr(db_obj, "status", "Error")
    else:
        # TODO handle other cases
        pass
    
    # timestamp is always updated
    setattr(db_obj, "last_update_at", datetime.now())
    setattr(db_obj, "timestamp", update_data["timestamp"])
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    return db_obj
