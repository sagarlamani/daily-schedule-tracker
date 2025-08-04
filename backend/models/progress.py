"""
Progress model for tracking user progress
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Progress(Base):
    """Progress database model."""
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    completion_rate = Column(Numeric(5, 2), default=0.00)
    total_time_minutes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress")

class ProgressResponse(BaseModel):
    """Pydantic model for progress responses."""
    id: int
    user_id: int
    date: date
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    total_time_minutes: int
    created_at: datetime
    
    class Config:
        from_attributes = True 