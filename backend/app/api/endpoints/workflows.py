from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db import crud, schemas
from app.api import dependencies as deps

router = APIRouter()



@router.get("/", response_model=List[schemas.Workflow])
async def get_workflows(
            offset: Optional[int] = 0,
            limit: Optional[int] = 100,
            session: AsyncSession = Depends(deps.get_session)):
    """Get multiple workflows

    Args:
        offset (Optional[int], optional): Offset into database rows. Defaults to 0.
        limit (Optional[int], optional): Limit of entries to get. Defaults to 100.
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Returns:
        List[schemas.Workflow]: List of workflow entries
    """
    workflows = await crud.read_workflow_multi(session, offset, limit)
    return workflows



@router.get("/{workflow_id}", response_model=schemas.Workflow)
async def get_workflow(
            workflow_id: int,
            session: AsyncSession = Depends(deps.get_session)):
    """Get single workflow by id

    Args:
        workflow_id (int): id / primary key of workflow
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Raises:
        HTTPException: Workflow not found

    Returns:
        schemas.Workflow: Workflow entry
    """
    workflow = await crud.read_workflow_single(session, workflow_id)

    if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow
