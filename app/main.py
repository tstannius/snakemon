from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pprint import pprint

#-----------------------------------------------------------------------------#
# db setup
#-----------------------------------------------------------------------------#
# db dependency - TODO: put elsewhere
from db import crud, models, schemas
from db.session import async_session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()


@app.get("/api/service-info", status_code=status.HTTP_200_OK)
async def service_info():
    return {"status": "running"}


@app.get("/create_workflow", status_code=status.HTTP_200_OK)
async def create_workflow(
        workflow: str,
        name: str,
        request: Request,
        session: AsyncSession = Depends(get_session)
        ):
    
    data = await request.form() # TODO: use metadata
    data = jsonable_encoder(data)
    
    db_workflow = await crud.create_workflow(session, workflow=schemas.WorkflowCreate(workflow=workflow, name=name))
    print(f"Creating workflow {db_workflow.workflow} with name {db_workflow.name}")
    return {"id": db_workflow.id}


@app.post("/update_workflow_status", status_code=status.HTTP_200_OK)
async def update_workflow_status(
        request: Request,
        session: AsyncSession = Depends(get_session)
        ):
    
    data = await request.form()
    data = jsonable_encoder(data)
    db_workflow = await crud.update_workflow(session, workflow=schemas.WorkflowUpdate(**data))
    return {"id": db_workflow.id}


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}
