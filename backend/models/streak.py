"""
Streak model for tracking user streaks
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Streak(Base):
    """Streak database model."""
    __tablename__ = "streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    streak_type = Column(String, nullable=False)  # daily, task
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)  # NULL for daily streaks
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_completed_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="streaks")
    task = relationship("Task", back_populates="streaks")

class StreakResponse(BaseModel):
    """Pydantic model for streak responses."""
    id: int
    user_id: int
    streak_type: str
    task_id: Optional[int] = None
    current_streak: int
    longest_streak: int
    last_completed_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 