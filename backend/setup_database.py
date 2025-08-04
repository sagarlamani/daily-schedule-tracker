#!/usr/bin/env python3
"""
Database setup script for Daily Schedule Tracker
This script creates the database and initializes it with the schema.
"""

import sqlite3
import os
from pathlib import Path

def setup_database():
    """Setup the database with schema and initial data."""
    
    # Get the database file path
    db_path = Path("schedule_tracker.db")
    
    print("🚀 Setting up Daily Schedule Tracker database...")
    
    # Read the schema file
    schema_file = Path("database/schema.sql")
    if not schema_file.exists():
        print("❌ Schema file not found!")
        return False
    
    try:
        with open(schema_file, 'r') as f:
            schema = f.read()
        
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute schema
        print("📋 Creating database tables...")
        cursor.executescript(schema)
        
        # Commit changes
        conn.commit()
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("✅ Database setup completed successfully!")
        print(f"📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Show some stats
        cursor.execute("SELECT COUNT(*) FROM categories;")
        category_count = cursor.fetchone()[0]
        print(f"📂 Added {category_count} default categories")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def reset_database():
    """Reset the database (delete and recreate)."""
    
    db_path = Path("schedule_tracker.db")
    
    if db_path.exists():
        print("🗑️  Removing existing database...")
        os.remove(db_path)
    
    return setup_database()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        success = reset_database()
    else:
        success = setup_database()
    
    if success:
        print("\n🎉 Database is ready to use!")
        print("💡 You can now start the backend server with: python main.py")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1) 