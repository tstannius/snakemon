"""CRUD utils - Create, Read, Update, Delete
"""
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from . import models, schemas


def create_workflow(db: Session, workflow: schemas.WorkflowCreate) -> models.Workflow:
    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

def update_workflow(db: Session, workflow: schemas.WorkflowUpdate) -> models.Workflow:
    obj_in = workflow
    db_obj = db.query(models.Workflow).get(obj_in.id)
    
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj