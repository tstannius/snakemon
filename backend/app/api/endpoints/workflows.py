from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db import crud, models, schemas
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
    workflows = await crud.read_multi_generic(session, 
                                              models.Workflow, 
                                              offset, 
                                              limit, 
                                              descending=True)
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
    workflow = await crud.read_generic(session, workflow_id, models.Workflow)

    if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow



@router.post("/{workflow_id}/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
async def create_comment(
            workflow_id: int,
            comment: schemas.CommentBase,
            user: models.User = Depends(deps.get_current_user),
            session: AsyncSession = Depends(deps.get_session)):
    """Create comment for workflow

    Args:
        workflow_id (int): id / primary key of workflow
        comment (schemas.CommentBase): Content of comment
        user (models.User, optional): User posting comment. Defaults to Depends(deps.get_current_user).
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Returns:
        schemas.Comment: Created comment
    """
    obj_in = schemas.CommentCreate(
                    workflow_id=workflow_id,
                    username=user.username,
                    **comment.dict())
    
    db_obj = await crud.create_generic(session, 
                                        obj_in=obj_in, 
                                        model=models.Comment)
    
    return db_obj



@router.get("/{workflow_id}/comments", status_code=status.HTTP_200_OK, response_model=List[schemas.Comment])
async def get_workflow_comments(
            workflow_id: int,
            session: AsyncSession = Depends(deps.get_session)):
    
    db_objs = await crud.read_workflow_relation_generic(
        session=session,
        foreign_key_id=workflow_id,
        model=models.Comment
    )

    if not db_objs:
        raise HTTPException(status_code=404, detail="Workflow or jobs not found")
    
    return [jsonable_encoder(j) for j in db_objs]
