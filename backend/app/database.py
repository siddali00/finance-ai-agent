"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import Config

# Build database URL from config
DATABASE_URL = (
    f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from app.models.db_models import Base
    Base.metadata.create_all(bind=engine)

