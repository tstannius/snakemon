from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pprint import pprint

#-----------------------------------------------------------------------------#
# db setup
#-----------------------------------------------------------------------------#
from db import crud, models, schemas
from db.database import engine, SessionLocal

# db dependency - TODO: put elsewhere
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()


@app.get("/api/service-info", status_code=status.HTTP_200_OK)
async def service_info():
    return {"status": "running"}


@app.get("/create_workflow", status_code=status.HTTP_200_OK)
async def create_workflow(workflow: str, name: str, request: Request, db: Session = Depends(get_db)):
    data = await request.form() # TODO: use metadata
    data = jsonable_encoder(data)
    print(data)
    db_workflow = crud.create_workflow(db, workflow=schemas.WorkflowCreate(workflow=workflow, name=name))
    print(f"Creating workflow {db_workflow.workflow} with name {db_workflow.name}")
    return {"id": db_workflow.id}


@app.post("/update_workflow_status", status_code=status.HTTP_200_OK)
async def update_workflow_status(request: Request, db: Session = Depends(get_db)):
    data = await request.form()
    data = jsonable_encoder(data)
    # db_workflow = crud.update_workflow(db, workflow=schemas.WorkflowUpdate(**da))
    print(data)
    # return {"id": db_workflow.id}


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}
