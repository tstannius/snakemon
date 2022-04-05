from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from collections import Counter

from app.db import crud, models, schemas
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
    jobs = await crud.read_relation_generic(
        session=session,
        model_from=models.Job,
        foreign_key_name="workflow_id",
        foreign_key_id=workflow_id,
        model_foreign=models.Workflow
    )

    if not jobs:
        raise HTTPException(status_code=404, detail="Workflow or jobs not found")
    
    jobs = [j.json() for j in jobs]
    return jobs



@router.get("/stats/")
async def get_workflow_jobs_stats(
            workflow_id: int,
            session: AsyncSession = Depends(deps.get_session)):
    """Get summary stats of jobs associated with workflow

    Args:
        workflow_id (int): id / primary key of workflow
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Raises:
        HTTPException: Workflow or jobs not found

    Returns:
        List[schemas.Job]: Workflow jobs
    """
    jobs = await crud.read_job_stats(
                session=session,
                workflow_id=workflow_id)
    
    workflow = await crud.read_generic(session, workflow_id, models.Workflow)

    if (not jobs) or (not workflow):
        raise HTTPException(status_code=404, detail="Workflow or jobs not found")
    
    counts = dict(Counter(jobs))
    
    stats = {
        "pending": (workflow.total - workflow.done - counts.get("Running", 0) - counts.get("Submitted", 0)), # submitted
        "submitted": None, # TODO: add for cluster feature
        "running": counts.get("Running", 0), # status is set as Running on creation
        "error": counts.get("Error"), # TODO: add for cluster feature
        "failed": None,
        "succeeded": counts.get("Done")
    }
    
    return stats
