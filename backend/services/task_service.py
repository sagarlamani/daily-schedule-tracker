"""
Task service for managing user tasks
"""

from database.connection import SessionLocal
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from typing import List, Optional

class TaskService:
    def get_user_tasks(self, user_id: int) -> List[Task]:
        """Get all tasks for a user."""
        db = SessionLocal()
        try:
            tasks = db.query(Task).filter(Task.user_id == user_id).all()
            return tasks
        finally:
            db.close()
    
    def get_task(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get a specific task."""
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            return task
        finally:
            db.close()
    
    def create_task(self, user_id: int, task_data: TaskCreate) -> Task:
        """Create a new task."""
        db = SessionLocal()
        try:
            task = Task(
                user_id=user_id,
                title=task_data.title,
                description=task_data.description,
                category_id=task_data.category_id,
                start_time=task_data.start_time,
                duration_minutes=task_data.duration_minutes,
                is_recurring=task_data.is_recurring,
                recurrence_pattern=task_data.recurrence_pattern,
                priority=task_data.priority
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
        finally:
            db.close()
    
    def update_task(self, task_id: int, user_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                return None
            
            # Update fields
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.category_id is not None:
                task.category_id = task_data.category_id
            if task_data.start_time is not None:
                task.start_time = task_data.start_time
            if task_data.duration_minutes is not None:
                task.duration_minutes = task_data.duration_minutes
            if task_data.is_recurring is not None:
                task.is_recurring = task_data.is_recurring
            if task_data.recurrence_pattern is not None:
                task.recurrence_pattern = task_data.recurrence_pattern
            if task_data.priority is not None:
                task.priority = task_data.priority
            
            db.commit()
            db.refresh(task)
            return task
        finally:
            db.close()
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task."""
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                return False
            
            db.delete(task)
            db.commit()
            return True
        finally:
            db.close()
    
    def complete_task(self, task_id: int, user_id: int) -> bool:
        """Mark a task as completed."""
        from datetime import datetime
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                return False
            
            task.is_completed = True
            task.completed_at = datetime.utcnow()
            db.commit()
            return True
        finally:
            db.close()
    
    def uncomplete_task(self, task_id: int, user_id: int) -> bool:
        """Mark a task as not completed."""
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                return False
            
            task.is_completed = False
            task.completed_at = None
            db.commit()
            return True
        finally:
            db.close()
    
    def check_time_conflicts(self, user_id: int, start_time: str, duration_minutes: int, exclude_task_id: int = None) -> List[dict]:
        """Check for time conflicts with existing tasks."""
        from datetime import datetime, timedelta
        
        db = SessionLocal()
        try:
            # Parse start time
            start_datetime = datetime.strptime(start_time, "%H:%M")
            
            # Calculate end time
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)
            
            # Get all user's tasks for the same day
            query = db.query(Task).filter(Task.user_id == user_id)
            
            # Exclude the current task if updating
            if exclude_task_id:
                query = query.filter(Task.id != exclude_task_id)
            
            existing_tasks = query.all()
            conflicts = []
            
            for task in existing_tasks:
                if task.is_completed:
                    continue  # Skip completed tasks
                
                # Parse existing task times
                task_start = datetime.strptime(task.start_time, "%H:%M")
                task_end = task_start + timedelta(minutes=task.duration_minutes)
                
                # Check for overlap
                if (start_datetime < task_end and end_datetime > task_start):
                    conflicts.append({
                        "task_id": task.id,
                        "title": task.title,
                        "start_time": task.start_time,
                        "duration_minutes": task.duration_minutes,
                        "overlap_type": "full" if (start_datetime <= task_start and end_datetime >= task_end) else "partial"
                    })
            
            return conflicts
        finally:
            db.close() 