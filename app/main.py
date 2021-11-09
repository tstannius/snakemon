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

# models.Base.metadata.create_all(bind=engine)

#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()


@app.get("/api/service-info", status_code=status.HTTP_200_OK)
async def service_info():
    return {"status": "running"}


@app.get("/create_workflow", status_code=status.HTTP_200_OK)
def create_workflow(workflow: str, name: str, db: Session = Depends(get_db)):
    db_workflow = crud.create_workflow(db, workflow=schemas.WorkflowCreate(workflow=workflow, name=name))
    print(f"Creating workflow {db_workflow.workflow} with name {db_workflow.name}")
    return {"id": db_workflow.id}


@app.post("/update_workflow_status", status_code=status.HTTP_200_OK)
async def update_workflow_status(req: Request):
    da = await req.form()
    da = jsonable_encoder(da)
    pprint(da)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}
