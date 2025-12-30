import os
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class SessionData:
    session_id: str
    uploaded_files: List[str] = field(default_factory=list)  # List of uploaded file paths
    dataframes: Dict[str, pd.DataFrame] = field(default_factory=dict)  # Sheet name -> DataFrame
    schema_info: Dict[str, Dict] = field(default_factory=dict)  # Sheet name -> Schema info
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)


class SessionManager:
    def __init__(self, upload_dir: str = "uploads"):
        self.sessions: Dict[str, SessionData] = {}
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    def create_session(self) -> str:
        """Create a new session and return session_id"""
        session_id = str(uuid.uuid4())
        session_path = os.path.join(self.upload_dir, session_id)
        os.makedirs(session_path, exist_ok=True)
        
        self.sessions[session_id] = SessionData(session_id=session_id)
        return session_id
    
    def get_session(self, session_id: str) -> SessionData:
        """Get session data by session_id"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        session.last_accessed = datetime.now()
        return session
    
    def update_session_data(
        self, 
        session_id: str, 
        file_path: Optional[str] = None,
        dataframes: Optional[Dict[str, pd.DataFrame]] = None,
        schema_info: Optional[Dict[str, Dict]] = None
    ):
        """Update session with file and parsed data. Merges with existing data."""
        session = self.get_session(session_id)
        
        if file_path:
            if file_path not in session.uploaded_files:
                session.uploaded_files.append(file_path)
        
        if dataframes:
            # Merge new dataframes with existing ones
            # If sheet name conflicts, prefix with filename
            for sheet_name, df in dataframes.items():
                if sheet_name in session.dataframes:
                    # Sheet name conflict - prefix with filename
                    file_basename = os.path.splitext(os.path.basename(file_path or "unknown"))[0]
                    new_sheet_name = f"{file_basename}_{sheet_name}"
                    session.dataframes[new_sheet_name] = df
                else:
                    session.dataframes[sheet_name] = df
        
        if schema_info:
            # Merge schema info similarly
            for sheet_name, info in schema_info.items():
                if sheet_name in session.schema_info:
                    # Sheet name conflict - prefix with filename
                    file_basename = os.path.splitext(os.path.basename(file_path or "unknown"))[0]
                    new_sheet_name = f"{file_basename}_{sheet_name}"
                    session.schema_info[new_sheet_name] = info
                else:
                    session.schema_info[sheet_name] = info
        
        session.last_accessed = datetime.now()
    
    def get_session_path(self, session_id: str) -> str:
        """Get the file storage path for a session"""
        return os.path.join(self.upload_dir, session_id)
    
    def cleanup_session(self, session_id: str):
        """Remove session and clean up files"""
        if session_id in self.sessions:
            session_path = self.get_session_path(session_id)
            if os.path.exists(session_path):
                import shutil
                shutil.rmtree(session_path)
            del self.sessions[session_id]

