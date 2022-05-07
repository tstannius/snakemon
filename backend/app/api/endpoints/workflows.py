from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional, Union

from app.db import crud, models, schemas
from app.api import dependencies as deps

router = APIRouter()



@router.get("", response_model=Dict[str, Union[List[schemas.Workflow], int]])
async def get_workflows(
            offset: Optional[int] = 0,
            limit: Optional[int] = 100,
            query: Optional[str] = None,
            session: AsyncSession = Depends(deps.get_session)):
    """Get multiple workflows
    
    TODO:
    - Add as parameters offset, limit, sorting, search string
    - Server should handle slice
    - Server must send back total page count.

    Args:
        offset (Optional[int], optional): Offset into database rows. Defaults to 0.
        limit (Optional[int], optional): Limit of entries to get. Defaults to 100.
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Returns:
        List[schemas.Workflow]: List of workflow entries
    """
    workflows, n_rows = await crud.read_multi_workflows(session=session,
                                              model=models.Workflow, 
                                              offset=offset, 
                                              limit=limit,
                                              query=query,
                                              descending=True)
    
    page_count = ceil(n_rows / limit)
    
    return {"workflows": workflows, "page_count": page_count}



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
                    user_id=user.id,
                    content=comment.content)
    
    db_obj = await crud.create_generic(session, 
                                        obj_in=obj_in, 
                                        model=models.Comment)
    
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Could not create comment")
    
    response = jsonable_encoder(db_obj)
    response["username"] = user.username # TODO: get from db
    return response



@router.get("/{workflow_id}/comments", status_code=status.HTTP_200_OK, response_model=List[schemas.Comment])
async def get_workflow_comments(
            workflow_id: int,
            session: AsyncSession = Depends(deps.get_session)):
    
    db_objs = await crud.read_owned_relation_generic(
        session=session,
        model_from=models.Comment,
        foreign_key_name="workflow_id",
        foreign_key_id=workflow_id,
        model_foreign=models.Workflow
    )

    # None if workflow not exists, 
    # empty list if exists, but no comments
    if db_objs is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    response = [{**jsonable_encoder(obj[0]), "username": obj[1].username} for obj in db_objs]
    return response

# TODO: update

@router.delete("/comments", status_code=status.HTTP_200_OK)
async def delete_comment(
            comment_id: int,
            user: models.User = Depends(deps.get_current_user),
            session: AsyncSession = Depends(deps.get_session)):
    """Delete comment

    Args:
        comment_id (int): id / primary key of comment
        user (models.User, optional): User posting comment. Defaults to Depends(deps.get_current_user).
        session (AsyncSession, optional): Database session. Defaults to Depends(deps.get_session).

    Returns:
        schemas.Comment: Deleted comment
    """  
    db_obj = await crud.delete_owned_generic(
                            session=session, 
                            obj_id=comment_id, 
                            user_id=user.id, 
                            model=models.Comment)
    
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    response = jsonable_encoder(db_obj)
    response["username"] = user.username
    from pprint import pprint
    pprint(response)
    return response
