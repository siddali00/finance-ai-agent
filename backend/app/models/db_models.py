"""
SQLAlchemy ORM models for PostgreSQL database
"""
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Session(Base):
    """Session table - stores session metadata"""
    __tablename__ = "sessions"
    
    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now)
    last_accessed = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    uploaded_files = relationship("UploadedFile", back_populates="session", cascade="all, delete-orphan")
    sheets = relationship("Sheet", back_populates="session", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="session", cascade="all, delete-orphan")


class UploadedFile(Base):
    """UploadedFile table - stores metadata about uploaded Excel files"""
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path to the stored file
    file_size = Column(Integer, nullable=False)  # File size in bytes
    uploaded_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    session = relationship("Session", back_populates="uploaded_files")
    sheets = relationship("Sheet", back_populates="uploaded_file", cascade="all, delete-orphan")


class Sheet(Base):
    """Sheet table - stores schema information for each sheet in uploaded files"""
    __tablename__ = "sheets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=True)
    sheet_name = Column(String, nullable=False)
    schema_info_json = Column(JSON, nullable=False)  # Store schema as JSON
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    session = relationship("Session", back_populates="sheets")
    uploaded_file = relationship("UploadedFile", back_populates="sheets")


class Conversation(Base):
    """Conversation table - stores query/response history"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    question = Column(Text, nullable=True)  # For query requests
    answer = Column(Text, nullable=True)  # Response from AI
    query_used = Column(Text, nullable=True)  # Generated pandas code
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    session = relationship("Session", back_populates="conversations")

