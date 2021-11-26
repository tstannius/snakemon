from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from db import schemas
from pprint import pprint

#-----------------------------------------------------------------------------#
# db setup
#-----------------------------------------------------------------------------#
# db dependency - TODO: put elsewhere
from db import crud, models, schemas
from db.session import async_session
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()

# origin: null - "... your server must read the value of the request's Origin 
# header and use that value to set Access-Control-Allow-Origin"
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin
origins = [
    "http://localhost:5000", # js serve uses port 5000 as default
    "http://localhost:3000", # react-scripts npm start uses port 3000 as default
    "null", # use null if running client app through a static html file, i.e. no server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"], # could also be '*'
    allow_headers=["*"],
)


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
    # TODO: use forms properly, see: https://github.com/tiangolo/fastapi/issues/2387
    # data = await request.form() # TODO: use metadata
    # data = jsonable_encoder(data)
    db_workflow = await crud.create_workflow(session, workflow=schemas.WorkflowCreate(workflow=workflow, name=name))
    print(f"Creating workflow {db_workflow.workflow} with name {db_workflow.name}")
    return {"id": db_workflow.id}


@app.post("/update_workflow_status", status_code=status.HTTP_200_OK)
async def update_workflow_status(
        workflow: schemas.WorkflowUpdate = Depends(schemas.WorkflowUpdate.as_form),
        session: AsyncSession = Depends(get_session)
        ):
    db_workflow = await crud.update_workflow(session, workflow=workflow)
    return {"id": db_workflow.id}


@app.get("/workflows", response_model=List[schemas.Workflow])
async def get_workflows(
            offset: Optional[int] = 0,
            limit: Optional[int] = 100,
            session: AsyncSession = Depends(get_session)):
    workflows = await crud.read_workflow_multi(session, offset, limit)
    return workflows


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}
