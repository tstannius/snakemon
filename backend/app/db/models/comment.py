from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1024))
    created_at = Column(DateTime, index=True)
    
    # relationships
    # don't delete on cascade, as comments should remain
    username = Column(Integer, ForeignKey('user.username'))
    # n.b. no need for back_populates="comments" for now
    user = relationship("User") # type: ignore
    workflow_id = Column(Integer, ForeignKey("workflow.id", ondelete="CASCADE"))
    workflow = relationship("Workflow", back_populates="comments")

    def __init__(self, workflow_id: int, username: str, content: str):
        self.content = content
        self.created_at = datetime.now()
        self.username = username
        self.workflow_id = workflow_id
