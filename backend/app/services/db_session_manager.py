"""
Database-backed session manager using PostgreSQL
Stores session metadata, file paths, and schema info in database
DataFrames are cached in memory for performance and reloaded from files when needed
"""
from sqlalchemy.orm import Session as DBSession
from app.models.db_models import Session as DBSessionModel, UploadedFile, Sheet, Conversation
from app.services.excel_parser import ExcelParser
import json
import pandas as pd
import os
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, field


@dataclass
class SessionData:
    """In-memory session data structure"""
    session_id: str
    uploaded_files: List[str] = field(default_factory=list)  # List of uploaded file paths
    dataframes: Dict[str, pd.DataFrame] = field(default_factory=dict)  # Sheet name -> DataFrame
    schema_info: Dict[str, Dict] = field(default_factory=dict)  # Sheet name -> Schema info
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)


class DBSessionManager:
    """
    Database-backed session manager.
    - Stores session metadata, file paths, and schema info in PostgreSQL
    - Caches DataFrames in memory for active sessions
    - Reloads DataFrames from files when server restarts (if files still exist)
    """
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
        self.excel_parser = ExcelParser()
        # In-memory cache for active sessions (DataFrames)
        self._dataframes_cache: Dict[str, Dict[str, pd.DataFrame]] = {}
        self._schema_cache: Dict[str, Dict[str, Dict]] = {}
    
    def create_session(self, db: DBSession) -> str:
        """Create a new session in database and return session_id"""
        session_id = str(uuid.uuid4())
        session_path = os.path.join(self.upload_dir, session_id)
        os.makedirs(session_path, exist_ok=True)
        
        db_session = DBSessionModel(
            session_id=session_id,
            created_at=datetime.now(),
            last_accessed=datetime.now()
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        # Initialize cache
        self._dataframes_cache[session_id] = {}
        self._schema_cache[session_id] = {}
        
        return session_id
    
    def get_session(self, db: DBSession, session_id: str) -> SessionData:
        """
        Get session data by session_id from database and load dataframes into cache.
        If session doesn't exist, raises ValueError.
        """
        # Check database
        db_session = db.query(DBSessionModel).filter(
            DBSessionModel.session_id == session_id
        ).first()
        
        if not db_session:
            raise ValueError(f"Session {session_id} not found")
        
        # Update last accessed
        db_session.last_accessed = datetime.now()
        db.commit()
        
        # Load dataframes and schema from DB into cache if not already there
        if session_id not in self._dataframes_cache:
            self._dataframes_cache[session_id] = {}
            self._schema_cache[session_id] = {}
            
            # Reload dataframes from files
            # Use composite key (filename_sheetname) to ensure uniqueness within session
            for uploaded_file in db_session.uploaded_files:
                if os.path.exists(uploaded_file.file_path):
                    # Parse the file again to get dataframes
                    file_dataframes = self.excel_parser.parse_excel(uploaded_file.file_path)
                    file_schema = self.excel_parser.extract_schema_info(file_dataframes)
                    
                    # Use composite key: filename_sheetname for uniqueness
                    file_basename = os.path.splitext(uploaded_file.filename)[0]
                    for sheet_name, df in file_dataframes.items():
                        cache_key = f"{file_basename}_{sheet_name}"
                        self._dataframes_cache[session_id][cache_key] = df
                    
                    # Update schema cache with same composite keys
                    for sheet_name, info in file_schema.items():
                        cache_key = f"{file_basename}_{sheet_name}"
                        self._schema_cache[session_id][cache_key] = info
                else:
                    # File was deleted, but schema info is still in DB
                    # Use composite key based on filename from DB
                    file_basename = os.path.splitext(uploaded_file.filename)[0]
                    for sheet in uploaded_file.sheets:
                        if sheet.schema_info_json:
                            cache_key = f"{file_basename}_{sheet.sheet_name}"
                            self._schema_cache[session_id][cache_key] = sheet.schema_info_json
        
        # Build SessionData from cache and DB
        session_data = SessionData(
            session_id=session_id,
            uploaded_files=[f.file_path for f in db_session.uploaded_files],
            dataframes=self._dataframes_cache[session_id],
            schema_info=self._schema_cache[session_id],
            created_at=db_session.created_at,
            last_accessed=db_session.last_accessed
        )
        
        return session_data
    
    def update_session_data(
        self,
        db: DBSession,
        session_id: str,
        file_path: Optional[str] = None,
        file_size: Optional[int] = None,
        dataframes: Optional[Dict[str, pd.DataFrame]] = None,
        schema_info: Optional[Dict[str, Dict]] = None
    ):
        """
        Update session with uploaded file data.
        Stores file metadata and schema in database, caches dataframes in memory.
        Sheets are uniquely identified by session_id + uploaded_file_id + sheet_name in DB.
        In memory cache, we use a composite key: filename_sheetname for uniqueness within session.
        """
        # Get or create session
        db_session = db.query(DBSessionModel).filter(
            DBSessionModel.session_id == session_id
        ).first()
        
        if not db_session:
            raise ValueError(f"Session {session_id} not found")
        
        if file_path:
            # Store file metadata
            filename = os.path.basename(file_path)
            # Get file size if file exists
            file_size = None
            if os.path.exists(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                except OSError:
                    pass  # File size unavailable
            
            # Use provided file_size or get it from file
            if file_size is None:
                if os.path.exists(file_path):
                    try:
                        file_size = os.path.getsize(file_path)
                    except OSError:
                        file_size = 0  # Default to 0 if can't get size
                else:
                    file_size = 0  # Default to 0 if file doesn't exist
            
            uploaded_file = UploadedFile(
                session_id=session_id,
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                uploaded_at=datetime.now()
            )
            db.add(uploaded_file)
            db.flush()  # Get the ID
            
            # Store schema info for each sheet
            # Sheets are uniquely identified by (session_id, uploaded_file_id, sheet_name) in DB
            # No conflicts possible since each file has its own uploaded_file_id
            if schema_info:
                file_basename = os.path.splitext(filename)[0]
                for sheet_name, sheet_schema in schema_info.items():
                    # Store original sheet name in DB (no need to modify - DB handles uniqueness via foreign keys)
                    sheet = Sheet(
                        session_id=session_id,
                        uploaded_file_id=uploaded_file.id,
                        sheet_name=sheet_name,  # Original sheet name - no conflict resolution needed
                        schema_info_json=sheet_schema
                    )
                    db.add(sheet)
        
        # Update cache - use composite key (filename_sheetname) for uniqueness in memory
        # This ensures sheets from different files with same name don't conflict
        if dataframes and file_path:
            if session_id not in self._dataframes_cache:
                self._dataframes_cache[session_id] = {}
            
            file_basename = os.path.splitext(os.path.basename(file_path))[0]
            for sheet_name, df in dataframes.items():
                # Use composite key: filename_sheetname to ensure uniqueness within session
                cache_key = f"{file_basename}_{sheet_name}"
                self._dataframes_cache[session_id][cache_key] = df
        
        if schema_info and file_path:
            if session_id not in self._schema_cache:
                self._schema_cache[session_id] = {}
            
            file_basename = os.path.splitext(os.path.basename(file_path))[0]
            for sheet_name, info in schema_info.items():
                # Use composite key: filename_sheetname to ensure uniqueness within session
                cache_key = f"{file_basename}_{sheet_name}"
                self._schema_cache[session_id][cache_key] = info
        
        # Update last accessed
        db_session.last_accessed = datetime.now()
        db.commit()
    
    def save_conversation(
        self,
        db: DBSession,
        session_id: str,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        query_used: Optional[str] = None
    ):
        """Save a conversation entry to the database"""
        conversation = Conversation(
            session_id=session_id,
            question=question,
            answer=answer,
            query_used=query_used,
            created_at=datetime.now()
        )
        db.add(conversation)
        db.commit()
    
    def get_or_create_session(self, db: DBSession, session_id: Optional[str] = None) -> str:
        """
        Get existing session or create a new one if session_id is None or invalid.
        Returns the session_id.
        """
        if session_id:
            # Validate UUID format
            try:
                uuid.UUID(session_id)
            except ValueError:
                # Invalid UUID format, create new session
                return self.create_session(db)
            
            # Check if session exists
            db_session = db.query(DBSessionModel).filter(
                DBSessionModel.session_id == session_id
            ).first()
            
            if db_session:
                return session_id
        
        # Create new session
        return self.create_session(db)

