#!/usr/bin/env python3
"""
Main FastAPI application for Daily Schedule Tracker
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from database.connection import get_db
from models.user import User
from models.category import Category
from models.task import Task, TaskCreate, TaskUpdate
from models.schedule import Schedule, ScheduleCreate, ScheduleUpdate
from models.streak import Streak
from models.progress import Progress
from services.auth_service import AuthService
from services.task_service import TaskService
from services.schedule_service import ScheduleService
from services.streak_service import StreakService
from services.progress_service import ProgressService

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting Daily Schedule Tracker API...")
    print(f"📊 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔗 Database: {os.getenv('DATABASE_URL', 'sqlite:///./schedule_tracker.db')}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Daily Schedule Tracker API...")

# Create FastAPI app
app = FastAPI(
    title="Daily Schedule Tracker API",
    description="A comprehensive API for tracking daily schedules, tasks, and streaks",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
auth_service = AuthService()
task_service = TaskService()
schedule_service = ScheduleService()
streak_service = StreakService()
progress_service = ProgressService()

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    try:
        token = credentials.credentials
        user = auth_service.verify_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "message": "Daily Schedule Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Authentication endpoints
@app.post("/api/auth/register")
async def register(user_data: dict):
    """Register a new user."""
    try:
        user = auth_service.register_user(user_data)
        return {"message": "User registered successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
async def login(credentials: dict):
    """Login user."""
    try:
        token = auth_service.login_user(credentials)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/api/auth/google")
async def google_auth(token_data: dict):
    """Authenticate with Google token."""
    try:
        user = auth_service.verify_google_token(token_data["token"])
        token = auth_service.create_token(user)
        return {"access_token": token, "token_type": "bearer", "user": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Task endpoints
@app.get("/api/tasks")
async def get_tasks(current_user: User = Depends(get_current_user)):
    """Get all tasks for the current user."""
    tasks = task_service.get_user_tasks(current_user.id)
    return {"tasks": tasks}

@app.post("/api/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task."""
    task = task_service.create_task(current_user.id, task_data)
    return {"message": "Task created successfully", "task": task}

@app.get("/api/tasks/{task_id}")
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific task."""
    task = task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@app.put("/api/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a task."""
    task = task_service.update_task(task_id, current_user.id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated successfully", "task": task}

@app.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete a task."""
    try:
        success = task_service.delete_task(task_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Mark a task as completed."""
    try:
        success = task_service.complete_task(task_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task marked as completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks/{task_id}/uncomplete")
async def uncomplete_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Mark a task as not completed."""
    try:
        success = task_service.uncomplete_task(task_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task marked as not completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Schedule endpoints
@app.get("/api/schedules/{date}")
async def get_schedule(
    date: str,
    current_user: User = Depends(get_current_user)
):
    """Get schedule for a specific date."""
    schedules = schedule_service.get_user_schedule(current_user.id, date)
    return {"schedules": schedules}

@app.post("/api/schedules")
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new schedule entry."""
    schedule = schedule_service.create_schedule(current_user.id, schedule_data)
    return {"message": "Schedule created successfully", "schedule": schedule}

@app.put("/api/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a schedule entry."""
    schedule = schedule_service.update_schedule(schedule_id, current_user.id, schedule_data)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule updated successfully", "schedule": schedule}

@app.post("/api/schedules/{schedule_id}/complete")
async def complete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user)
):
    """Mark a schedule as completed."""
    result = schedule_service.complete_schedule(schedule_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Update streaks
    streak_service.update_streaks(current_user.id, schedule_id)
    
    return {"message": "Schedule completed successfully", "streak_updated": True}

# Streak endpoints
@app.get("/api/streaks")
async def get_streaks(current_user: User = Depends(get_current_user)):
    """Get all streaks for the current user."""
    streaks = streak_service.get_user_streaks(current_user.id)
    return {"streaks": streaks}

@app.get("/api/streaks/daily")
async def get_daily_streak(current_user: User = Depends(get_current_user)):
    """Get daily streak for the current user."""
    streak = streak_service.get_daily_streak(current_user.id)
    return {"streak": streak}

# Progress endpoints
@app.get("/api/progress/{date}")
async def get_progress(
    date: str,
    current_user: User = Depends(get_current_user)
):
    """Get progress for a specific date."""
    progress = progress_service.get_user_progress(current_user.id, date)
    return {"progress": progress}

@app.get("/api/progress/weekly")
async def get_weekly_progress(current_user: User = Depends(get_current_user)):
    """Get weekly progress for the current user."""
    progress = progress_service.get_weekly_progress(current_user.id)
    return {"progress": progress}

@app.get("/api/progress/monthly")
async def get_monthly_progress(current_user: User = Depends(get_current_user)):
    """Get monthly progress for the current user."""
    progress = progress_service.get_monthly_progress(current_user.id)
    return {"progress": progress}

# Analytics endpoints
@app.get("/api/analytics/summary")
async def get_analytics_summary(current_user: User = Depends(get_current_user)):
    """Get analytics summary for the current user."""
    summary = progress_service.get_analytics_summary(current_user.id)
    return {"summary": summary}

@app.get("/api/analytics/categories")
async def get_category_analytics(current_user: User = Depends(get_current_user)):
    """Get category-wise analytics."""
    analytics = progress_service.get_category_analytics(current_user.id)
    return {"analytics": analytics}

# Categories endpoints
@app.get("/api/categories")
async def get_categories():
    """Get all categories."""
    try:
        db = next(get_db())
        categories = db.query(Category).all()
        return {"categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "color": cat.color,
                "icon": cat.icon
            } for cat in categories
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Template endpoints
@app.get("/api/templates")
async def get_templates():
    """Get available schedule templates."""
    templates = [
        {
            "id": "student",
            "name": "Student Schedule",
            "description": "Balanced schedule for students",
            "tasks": [
                {"title": "Morning Study", "time": "08:00", "duration": 60, "category": "Study"},
                {"title": "Classes", "time": "10:00", "duration": 180, "category": "Study"},
                {"title": "Lunch Break", "time": "13:00", "duration": 60, "category": "Personal"},
                {"title": "Afternoon Study", "time": "14:00", "duration": 120, "category": "Study"},
                {"title": "Exercise", "time": "16:30", "duration": 60, "category": "Exercise"},
                {"title": "Evening Review", "time": "19:00", "duration": 90, "category": "Study"}
            ]
        },
        {
            "id": "professional",
            "name": "Professional Schedule",
            "description": "Productive work schedule",
            "tasks": [
                {"title": "Morning Routine", "time": "07:00", "duration": 60, "category": "Personal"},
                {"title": "Work Start", "time": "09:00", "duration": 240, "category": "Work"},
                {"title": "Lunch Break", "time": "13:00", "duration": 60, "category": "Personal"},
                {"title": "Afternoon Work", "time": "14:00", "duration": 240, "category": "Work"},
                {"title": "Exercise", "time": "18:00", "duration": 60, "category": "Exercise"},
                {"title": "Evening Planning", "time": "20:00", "duration": 30, "category": "Work"}
            ]
        },
        {
            "id": "fitness",
            "name": "Fitness Focus",
            "description": "Health and fitness oriented schedule",
            "tasks": [
                {"title": "Morning Workout", "time": "06:00", "duration": 60, "category": "Exercise"},
                {"title": "Breakfast", "time": "07:30", "duration": 30, "category": "Health"},
                {"title": "Work", "time": "09:00", "duration": 240, "category": "Work"},
                {"title": "Lunch", "time": "13:00", "duration": 60, "category": "Health"},
                {"title": "Afternoon Work", "time": "14:00", "duration": 240, "category": "Work"},
                {"title": "Evening Workout", "time": "18:00", "duration": 60, "category": "Exercise"},
                {"title": "Dinner", "time": "19:30", "duration": 60, "category": "Health"}
            ]
        }
    ]
    return {"templates": templates}

if __name__ == "__main__":
    # Run the application
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    ) 