"""SQLAlchemy database models

These models define the database tables
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # TODO: consider making django-like table name
        # Alembic and FastAPI will still know what to do
        return cls.__name__.lower()


class Job(Base):
    id = Column(Integer, primary_key=True)
    jobid = Column(Integer, unique=False)
    workflow_id = Column(Integer, ForeignKey('workflow.id'))
    
    msg = Column(String(100), unique=False)
    name = Column(String(40), unique=False)
    # local = Column(Boolean(), unique=False)
    input = Column(String(1000), unique=False)
    output = Column(String(1000), unique=False)
    
    log = Column(String(100), unique=False) # path to log
    benchmark = Column(String(100), unique=False) # path to benchmark
    wildcards = Column(String(100), unique=False) # dict of wildcards
    wildcard_id = Column(String(100), unique=False) # sample identifier
    
    # reason for job execution
    
    # resources
    # need to parse to extract X mem, X walltime, path
    # priority
    # threads
    # indent?
    # printshellcmd
    # is_handover
    
    shell_command = Column(String(100), unique=False)
    is_checkpoint = Column(Boolean, unique=False)
    
    # meta info
    status = Column(String(30), unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_update_at = Column(DateTime)
    
    workflow = relationship("Workflow", back_populates="jobs")
    
    def __init__(self, workflow_id, jobid, msg, name, input, output, log, 
                 benchmark, wildcards, shell_command, is_checkpoint, 
                 status="Running"):
        self.jobid = jobid
        self.workflow_id = workflow_id
        self.msg = msg
        self.name = name
        self.input = ','.join(input) # TODO: fix type, this is list
        self.output = ','.join(output)
        self.log = ','.join(log)
        self.benchmark = benchmark
        self.wildcards = ','.join([f"{k}:{v}" for k,v in wildcards.items()])
        self.wildcard_id = None # TODO: infer from wildcards and env?
        self.is_checkpoint = is_checkpoint
        self.shell_command = shell_command
        self.status = status
        self.started_at = datetime.now()
        self.last_update_at = datetime.now()


class Workflow(Base):
    id = Column(Integer, primary_key=True)
    workflow = Column(String(50), unique=False)
    name = Column(String(50), unique=False)
    status = Column(String(30), unique=False)
    done = Column(Integer, unique=False)
    total = Column(Integer, unique=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_update_at = Column(DateTime)
    timestamp = Column(String(30))
    
    jobs = relationship("Job", back_populates="workflow")

    def __init__(self, workflow, name):
        self.workflow = workflow
        self.name = name
        self.done = 0
        self.total = 0
        self.started_at = datetime.now()
        self.last_update_at = datetime.now()
