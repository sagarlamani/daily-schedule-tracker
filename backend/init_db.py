#!/usr/bin/env python3
"""
Database initialization script for Railway deployment
"""

import os
import sys
from sqlalchemy import text
from database.connection import engine, SessionLocal
from models.user import User
from models.category import Category
from models.task import Task
from models.schedule import Schedule
from models.streak import Streak
from models.progress import Progress

def init_database():
    """Initialize the database with tables and default data."""
    print("🚀 Initializing database...")
    
    try:
        # Create all tables
        from database.connection import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        
        # Initialize default categories
        db = SessionLocal()
        
        # Check if categories already exist
        existing_categories = db.query(Category).count()
        if existing_categories == 0:
            print("📝 Adding default categories...")
            
            default_categories = [
                Category(name="Work", color="#3B82F6", icon="💼"),
                Category(name="Study", color="#10B981", icon="📚"),
                Category(name="Exercise", color="#F59E0B", icon="🏃‍♂️"),
                Category(name="Personal", color="#8B5CF6", icon="👤"),
                Category(name="Health", color="#EF4444", icon="❤️"),
                Category(name="Social", color="#06B6D4", icon="👥"),
                Category(name="Hobby", color="#84CC16", icon="🎨"),
                Category(name="Other", color="#6B7280", icon="📌")
            ]
            
            for category in default_categories:
                db.add(category)
            
            db.commit()
            print("✅ Default categories added")
        else:
            print("ℹ️ Categories already exist, skipping...")
        
        db.close()
        print("🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database() 