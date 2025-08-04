"""
Progress service for tracking user progress
"""

from database.connection import SessionLocal
from models.progress import Progress
from datetime import date
from typing import List, Optional, Dict

class ProgressService:
    def get_user_progress(self, user_id: int, date: str) -> Optional[Progress]:
        """Get progress for a specific date."""
        db = SessionLocal()
        try:
            progress = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.date == date
            ).first()
            return progress
        finally:
            db.close()
    
    def get_weekly_progress(self, user_id: int) -> List[Progress]:
        """Get weekly progress for a user."""
        # For testing, return empty list
        return []
    
    def get_monthly_progress(self, user_id: int) -> List[Progress]:
        """Get monthly progress for a user."""
        # For testing, return empty list
        return []
    
    def get_analytics_summary(self, user_id: int) -> Dict:
        """Get analytics summary for a user."""
        # For testing, return mock data
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "completion_rate": 0.0,
            "total_time": 0,
            "current_streak": 0,
            "longest_streak": 0
        }
    
    def get_category_analytics(self, user_id: int) -> List[Dict]:
        """Get category-wise analytics."""
        # For testing, return mock data
        return [
            {"category": "Work", "tasks": 0, "time": 0},
            {"category": "Study", "tasks": 0, "time": 0},
            {"category": "Exercise", "tasks": 0, "time": 0}
        ] 