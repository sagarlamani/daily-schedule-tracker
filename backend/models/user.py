"""
User model for authentication and user management
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    provider = Column(String, default="email")  # email, google
    hashed_password = Column(String, nullable=True)  # Only for email auth
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="user")
    schedules = relationship("Schedule", back_populates="user")
    streaks = relationship("Streak", back_populates="user")
    progress = relationship("Progress", back_populates="user")

class UserCreate(BaseModel):
    """Pydantic model for user creation."""
    email: EmailStr
    name: str
    password: Optional[str] = None
    provider: str = "email"
    avatar_url: Optional[str] = None

class UserUpdate(BaseModel):
    """Pydantic model for user updates."""
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    """Pydantic model for user responses."""
    id: int
    email: str
    name: str
    avatar_url: Optional[str] = None
    provider: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Pydantic model for user login."""
    email: EmailStr
    password: str 