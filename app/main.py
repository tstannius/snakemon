import uuid
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pprint import pprint
# from fastapi.middleware.cors import CORSMiddleware

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

models.Base.metadata.create_all(bind=engine)

#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()

# origin: null - "... your server must read the value of the request's Origin 
# header and use that value to set Access-Control-Allow-Origin"
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin
# origins = [
#     "http://localhost:5000", # js serve uses port 5000 as default
#     "http://localhost:3000", # react-scripts start uses port 3000 as default
#     "null", # use null if running client app through a static html file, i.e. no server
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET"], # could also be '*'
#     allow_headers=["*"],
# )

class WorkflowUpdate(BaseModel):
    # 'msg': repr(msg),
    # 'timestamp': time.asctime(),
    # 'id': id
    id: str
    timestamp: str
    msg: str



@app.get("/api/service-info", status_code=status.HTTP_200_OK)
async def service_info():
    return {"status": "running"}


@app.get("/create_workflow", status_code=status.HTTP_200_OK)
async def create_workflow(workflow: str, name: str, db: Session = Depends(get_db)):
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
