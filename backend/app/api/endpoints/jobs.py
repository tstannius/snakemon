from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db import crud, schemas
from app.api import dependencies as deps

router = APIRouter()
from fastapi.encoders import jsonable_encoder


@router.get("/", response_model=List[schemas.Job])
async def get_workflow_jobs(
            workflow_id: int,
            session: AsyncSession = Depends(deps.get_session)):
    """Get jobs associated with workflow

    Args:
        workflow_id (int): id / primary key of workflow
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Raises:
        HTTPException: Workflow not found

    Returns:
        List[schemas.Job]: Workflow jobs
    """
    jobs = await crud.read_workflow_jobs(session, workflow_id)

    if not jobs:
        raise HTTPException(status_code=404, detail="Workflow or jobs not found")
    
    jobs = [j.json() for j in jobs]
    return jobs
