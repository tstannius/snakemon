from datetime import datetime
from pydantic import BaseModel



class CommentBase(BaseModel):
    content: str
    
    class Config:
        orm_mode = True



class CommentCreate(CommentBase):
    # user_id: int
    username: str
    workflow_id: int
    
    class Config:
        orm_mode = True



class Comment(CommentCreate):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
