"""
Task model for managing user tasks
"""

from sqlalchemy import Column, Integer, String, Text, Time, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class Task(Base):
    """Task database model."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, default=30, nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)  # daily, weekly, monthly
    priority = Column(String, default="medium")  # low, medium, high
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    schedules = relationship("Schedule", back_populates="task")
    streaks = relationship("Streak", back_populates="task")

class TaskCreate(BaseModel):
    """Pydantic model for task creation."""
    title: str
    description: Optional[str] = None
    category_id: int
    start_time: time
    duration_minutes: int = 30
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    priority: str = "medium"

class TaskUpdate(BaseModel):
    """Pydantic model for task updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    priority: Optional[str] = None

class TaskResponse(BaseModel):
    """Pydantic model for task responses."""
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    category_id: int
    start_time: time
    duration_minutes: int
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    priority: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 