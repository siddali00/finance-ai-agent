"""
Initialize database tables
Run this script to create all necessary tables in PostgreSQL
"""
from app.database import init_db

if __name__ == "__main__":
    print("Initializing database tables...")
    init_db()
    print("Database tables created successfully!")

