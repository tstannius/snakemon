from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class Job(BaseModel):
    jobid: int
    workflow_id: int
    
    class Config:
        orm_mode = True


class JobCreate(Job):
    msg: Optional[str] = None
    name: Optional[str] = None
    # local 
    input: Optional[List[str]] = None # TODO use path type?
    output: Optional[List[str]] = None # TODO use path type?
    
    log: Optional[List[str]] = None
    benchmark: Optional[str] = None
    wildcards: Optional[Dict[str, str]] = None
    # wildcard_id: Optional[str] = None # TODO: find out where to put this
    
    # reason for job execution
    
    # resources
    # need to parse to extract threads, mem, walltime, path
    # priority
    # threads
    # indent?
    # printshellcmd
    # is_handover
    
    shell_command: Optional[str] = None
    is_checkpoint: Optional[bool] = None
    
    class Config:
        orm_mode = True
        

class JobUpdate(Job):
    completed_at: Optional[datetime] = None
    last_update_at: datetime = datetime.now()
    status: str
    
    class Config:
        orm_mode = True
