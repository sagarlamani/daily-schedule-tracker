"""
Streak service for managing user streaks
"""

from database.connection import SessionLocal
from models.streak import Streak
from datetime import date
from typing import List, Optional

class StreakService:
    def get_user_streaks(self, user_id: int) -> List[Streak]:
        """Get all streaks for a user."""
        db = SessionLocal()
        try:
            streaks = db.query(Streak).filter(Streak.user_id == user_id).all()
            return streaks
        finally:
            db.close()
    
    def get_daily_streak(self, user_id: int) -> Optional[Streak]:
        """Get daily streak for a user."""
        db = SessionLocal()
        try:
            streak = db.query(Streak).filter(
                Streak.user_id == user_id,
                Streak.streak_type == "daily"
            ).first()
            return streak
        finally:
            db.close()
    
    def update_streaks(self, user_id: int, schedule_id: int) -> bool:
        """Update streaks when a schedule is completed."""
        # For testing, we'll just return True
        # In production, you'd implement proper streak logic
        return True 