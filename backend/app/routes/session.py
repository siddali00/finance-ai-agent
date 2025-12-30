from fastapi import APIRouter, Depends
from app.models.schemas import SessionResponse
from app.services.shared import db_session_manager
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["session"])


@router.get("/session", response_model=SessionResponse)
async def create_session(db: Session = Depends(get_db)):
    """Create a new session and return session_id"""
    session_id = db_session_manager.create_session(db)
    return SessionResponse(session_id=session_id)

