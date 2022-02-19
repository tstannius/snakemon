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
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # user = relationship("User", back_populates="comments") # type: ignore
    user = relationship("User") # type: ignore
    
    workflow_id = Column(Integer, ForeignKey("workflow.id", ondelete="CASCADE"))
    workflow = relationship("Workflow", back_populates="comments")

    def __init__(self, workflow_id: int, user_id: str, content: str):
        self.content = content
        self.created_at = datetime.now()
        self.user_id = user_id
        self.workflow_id = workflow_id
