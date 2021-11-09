"""CRUD utils - Create, Read, Update, Delete
"""
from sqlalchemy.orm import Session

from . import models, schemas


def create_workflow(db: Session, workflow: schemas.WorkflowCreate):
    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

