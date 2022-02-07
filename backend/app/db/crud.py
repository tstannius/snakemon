"""CRUD utils - Create, Read, Update, Delete
"""
# TODO do type ignore in mypy config, see https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-type-hints-for-third-party-library
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import select # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from datetime import datetime

from . import models, schemas

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)



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



async def create_generic(session: AsyncSession, 
                         obj_in: CreateSchemaType, 
                         model: Type[ModelType]) -> ModelType:
    """Create generic

    Args:
        session (AsyncSession): Database session
        obj_in (CreateSchemaType): Schema of object to create
        model (Type[ModelType]): Database model type

    Returns:
        ModelType: Created database model object
    """
    # create db model obj
    obj_in_data = jsonable_encoder(obj_in) # safer than dict()
    db_obj = model(**obj_in_data)  # type: ignore
    # add, commit and refresh db
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj



async def read_generic(session: AsyncSession, obj_id: Any, model: Type[ModelType]) -> Optional[ModelType]:
    """Read single object from database

    Args:
        session (AsyncSession): Database session
        obj_id (Any): Primary key of object
        model (Type[ModelType]): Database model type

    Returns:
        Optional[ModelType]: Database entry if exists, else None
    """
    query = await session.execute(
            select(model)
                .where(model.id == obj_id)
        )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj: Optional[model] = query.scalars().first()
    return db_obj



async def read_multi_generic(session: AsyncSession, 
                             model: Type[ModelType],
                             offset: Optional[int]=0, 
                             limit: Optional[int]=100,
                             descending=False) -> List[models.Workflow]:
    """Read multiple objects from database

    Args:
        session (AsyncSession): Database session
        model (Type[ModelType]): Database model type
        offset (Optional[int], optional): Offset into database rows. Defaults to 0.
        limit (Optional[int], optional): Limit number of workflows returned. Defaults to 100.

    Returns:
        List[models.Workflow]: List of entries in database
    """
    # TODO: more elegant approach for sorting
    if descending:
        result = await session.execute(
                select(model).order_by(model.id.desc()).offset(offset).limit(limit)
            )
    else:
        result = await session.execute(
                select(model).order_by(model.id).offset(offset).limit(limit)
            )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj_list: Optional[List[model]] = result.scalars().all()
    return db_obj_list



async def read_workflow_relation_generic(session: AsyncSession, 
                                foreign_key_id: Any,
                                model: Type[ModelType]) -> Optional[ModelType]:
    """Read objects related with given workflow

    Args:
        session (AsyncSession): Database session
        foreign_key_id (Any): Primary key of workflow
        model (Type[ModelType]): Database model type

    Returns:
        Optional[ModelType]: List of database objects of given model type
    """
   
    result = await session.execute(
            select(model)
                .where(model.workflow_id == foreign_key_id)
        )
    # Note the use of .scalars() to get ScarlarResult, i.e. Pydantic model, instead of Row object
    db_obj_list: Optional[List[model]] = result.scalars().all()
    
    return db_obj_list



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
        await create_generic(session=session, 
                             obj_in=schemas.JobCreate(**{"workflow_id": workflow.id, **workflow.msg}),
                             model=models.Job)
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
