"""
Schedule model for managing daily schedule instances
"""

from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class Schedule(Base):
    """Schedule database model."""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String, default="pending")  # pending, completed, skipped, overdue
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    task = relationship("Task", back_populates="schedules")
    user = relationship("User", back_populates="schedules")

class ScheduleCreate(BaseModel):
    """Pydantic model for schedule creation."""
    task_id: int
    scheduled_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = None

class ScheduleUpdate(BaseModel):
    """Pydantic model for schedule updates."""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ScheduleResponse(BaseModel):
    """Pydantic model for schedule responses."""
    id: int
    task_id: int
    user_id: int
    scheduled_date: date
    start_time: time
    end_time: time
    status: str
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True 