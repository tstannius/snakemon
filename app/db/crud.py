"""CRUD utils - Create, Read, Update, Delete
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from typing import Optional
from . import models, schemas


async def create_workflow(session: AsyncSession, workflow: schemas.WorkflowCreate) -> models.Workflow:
    db_workflow = models.Workflow(**workflow.dict())
    session.add(db_workflow)
    await session.commit()
    await session.refresh(db_workflow)
    return db_workflow

async def update_workflow(session: AsyncSession, workflow: schemas.WorkflowUpdate) -> models.Workflow:
    obj_in = workflow
    query = await session.execute(
            select(models.Workflow).where(models.Workflow.id == obj_in.id)
        )
    db_obj: Optional[models.Workflow] = query.scalars().first()
    
    update_data = obj_in.dict(exclude_unset=True)
    setattr(db_obj, "last_update_at", update_data["timestamp"]) # TODO rename to timestamp?
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    return db_obj