from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud, schemas
from app.api import dependencies as deps

router = APIRouter()

@router.get("/api/service-info", status_code=status.HTTP_200_OK)
async def service_info():
    """Check if service is running
    Used by snakemake to check if posts will be received
    """
    return {"status": "running"}


@router.get("/create_workflow", status_code=status.HTTP_200_OK)
async def create_workflow(
        workflow: str,
        name: str,
        request: Request,
        session: AsyncSession = Depends(deps.get_session)
        ):
    """Create a new workflow

    Returns:
        id: primary key of newly created workflow
    """
    # TODO: use forms properly, see: https://github.com/tiangolo/fastapi/issues/2387
    # data = await request.form() # TODO: use metadata
    # data = jsonable_encoder(data)
    db_workflow = await crud.create_workflow(session, workflow=schemas.WorkflowCreate(workflow=workflow, name=name))
    print(f"Creating workflow {db_workflow.workflow} with name {db_workflow.name}")
    return {"id": db_workflow.id}


@router.post("/update_workflow_status", status_code=status.HTTP_200_OK)
async def update_workflow_status(
        workflow: schemas.WorkflowUpdate = Depends(schemas.WorkflowUpdate.as_form),
        session: AsyncSession = Depends(deps.get_session)
        ):
    """Update workflow status

    Updates sent from snakemake contain the workflow id provided by the backend,
    as well as a msg (dict which may contain any kind of update) and a timestamp
    """
    db_workflow = await crud.update_workflow(session, workflow=workflow)
    return {"id": db_workflow.id}
