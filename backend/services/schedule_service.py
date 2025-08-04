"""
Schedule service for managing daily schedules
"""

from database.connection import SessionLocal
from models.schedule import Schedule, ScheduleCreate, ScheduleUpdate
from datetime import datetime
from typing import List, Optional

class ScheduleService:
    def get_user_schedule(self, user_id: int, date: str) -> List[Schedule]:
        """Get schedule for a specific date."""
        db = SessionLocal()
        try:
            schedules = db.query(Schedule).filter(
                Schedule.user_id == user_id,
                Schedule.scheduled_date == date
            ).all()
            return schedules
        finally:
            db.close()
    
    def create_schedule(self, user_id: int, schedule_data: ScheduleCreate) -> Schedule:
        """Create a new schedule entry."""
        db = SessionLocal()
        try:
            schedule = Schedule(
                task_id=schedule_data.task_id,
                user_id=user_id,
                scheduled_date=schedule_data.scheduled_date,
                start_time=schedule_data.start_time,
                end_time=schedule_data.end_time,
                notes=schedule_data.notes
            )
            db.add(schedule)
            db.commit()
            db.refresh(schedule)
            return schedule
        finally:
            db.close()
    
    def update_schedule(self, schedule_id: int, user_id: int, schedule_data: ScheduleUpdate) -> Optional[Schedule]:
        """Update a schedule entry."""
        db = SessionLocal()
        try:
            schedule = db.query(Schedule).filter(
                Schedule.id == schedule_id,
                Schedule.user_id == user_id
            ).first()
            if not schedule:
                return None
            
            # Update fields
            if schedule_data.start_time is not None:
                schedule.start_time = schedule_data.start_time
            if schedule_data.end_time is not None:
                schedule.end_time = schedule_data.end_time
            if schedule_data.status is not None:
                schedule.status = schedule_data.status
            if schedule_data.notes is not None:
                schedule.notes = schedule_data.notes
            
            db.commit()
            db.refresh(schedule)
            return schedule
        finally:
            db.close()
    
    def complete_schedule(self, schedule_id: int, user_id: int) -> bool:
        """Mark a schedule as completed."""
        db = SessionLocal()
        try:
            schedule = db.query(Schedule).filter(
                Schedule.id == schedule_id,
                Schedule.user_id == user_id
            ).first()
            if not schedule:
                return False
            
            schedule.status = "completed"
            schedule.completed_at = datetime.utcnow()
            
            db.commit()
            return True
        finally:
            db.close() 