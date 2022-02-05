from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import json
from .base import Base



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
    
    workflow = relationship("Workflow", back_populates="jobs") # type: ignore
    
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
        self.wildcards = json.dumps(wildcards)
        self.wildcard_id = None # TODO: infer from wildcards and env?
        self.is_checkpoint = is_checkpoint
        self.shell_command = shell_command
        self.status = status
        self.started_at = datetime.now()
        self.last_update_at = datetime.now()
        
    def json(self):
        return {
            "id": self.id,
            "jobid": self.jobid,
            "workflow_id": self.workflow_id,
            "msg": self.msg,
            "name": self.name,
            "input": self.input.split(','),
            "output": self.input.split(','),
            "log": self.log.split(','),
            "benchmark": self.benchmark,
            "wildcards": json.loads(self.wildcards),
            "shell_command": self.shell_command,
            "is_checkpoint": self.is_checkpoint,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "last_update_at": self.last_update_at
        }
