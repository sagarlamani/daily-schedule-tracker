"""
Category model for task categories
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Category(Base):
    """Category database model."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#3b82f6")  # hex color
    icon = Column(String, default="circle")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="category")

class CategoryResponse(BaseModel):
    """Pydantic model for category responses."""
    id: int
    name: str
    color: str
    icon: str
    created_at: datetime
    
    class Config:
        from_attributes = True 