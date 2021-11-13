"""CRUD utils - Create, Read, Update, Delete
"""
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from . import models, schemas


async def create_workflow(session: AsyncSession, workflow: schemas.WorkflowCreate) -> models.Workflow:
    db_workflow = models.Workflow(**workflow.dict())
    session.add(db_workflow)
    await session.commit()
    await session.refresh(db_workflow)
    return db_workflow

async def update_workflow(session: AsyncSession, workflow: schemas.WorkflowUpdate) -> models.Workflow:
    obj_in = workflow
    db_obj = obj_in
    # db_obj = db.query(models.Workflow).get(obj_in.id)
    
    # obj_data = jsonable_encoder(db_obj)
    # if isinstance(obj_in, dict):
    #     update_data = obj_in
    # else:
    #     update_data = obj_in.dict(exclude_unset=True)
    # for field in obj_data:
    #     if field in update_data:
    #         setattr(db_obj, field, update_data[field])
    # db.add(db_obj)
    # db.commit()
    # db.refresh(db_obj)
    return db_obj