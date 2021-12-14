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
    workflows = await crud.read_workflow_multi(session, offset, limit)
    return workflows
