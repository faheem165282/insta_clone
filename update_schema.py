"""
Script to add missing columns to the Photo table without using Flask-Migrate
"""
import sys
from src import create_app, db
import sqlalchemy
from sqlalchemy.exc import OperationalError

# Force immediate output flushing
sys.stdout.reconfigure(line_buffering=True)

print("Starting database schema update...")
app = create_app()

with app.app_context():
    print("Connecting to database...")
    # Get database connection
    connection = db.engine.connect()
    print("Connection established!")
    
    try:
        # Check if media_type column exists
        print("Checking for media_type column...")
        try:
            connection.execute(sqlalchemy.text("SELECT media_type FROM photo LIMIT 1"))
            print("media_type column already exists")
        except OperationalError:
            # Add media_type column
            print("Adding media_type column...")
            connection.execute(sqlalchemy.text(
                "ALTER TABLE photo ADD COLUMN media_type VARCHAR(10) DEFAULT 'photo'"
            ))
            connection.commit()
            print("media_type column added successfully")
        
        # Check if file_size column exists
        print("Checking for file_size column...")
        try:
            connection.execute(sqlalchemy.text("SELECT file_size FROM photo LIMIT 1"))
            print("file_size column already exists")
        except OperationalError:
            # Add file_size column
            print("Adding file_size column...")
            connection.execute(sqlalchemy.text(
                "ALTER TABLE photo ADD COLUMN file_size INTEGER DEFAULT 0"
            ))
            connection.commit()
            print("file_size column added successfully")
        
        print("Database schema update completed!")
        
    except Exception as e:
        print(f"Error updating database schema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.close()
        print("Database connection closed")
