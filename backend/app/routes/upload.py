from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from typing import List, Optional
from app.models.schemas import UploadResponse, FileUploadInfo
from app.services.shared import db_session_manager, excel_parser
from app.config import Config
from app.database import get_db
from sqlalchemy.orm import Session
import os
import shutil

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: List[UploadFile] = File(...),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload one or more Excel files for a session
    Supports multiple file uploads - all files will be merged into the session
    If session_id is not provided or invalid, a new session will be created
    
    Note: Use form field name "file" for single or multiple files
    """
    # Get or create session
    session_id = db_session_manager.get_or_create_session(db, session_id)
    
    # Handle both single file (if sent as single) and multiple files
    files = file if isinstance(file, list) else [file]
    
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_files_info = []
    all_sheets = []
    all_schema_info = {}
    errors = []
    all_dataframes = {}
    
    # Process each file
    for file in files:
        try:
            # Validate file type
            if not file.filename:
                errors.append(f"One or more files have no filename")
                continue
            
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in ['.xlsx', '.xls']:
                errors.append(f"{file.filename}: Only .xlsx and .xls files are supported")
                continue
            
            # Read file content to check size
            content = await file.read()
            file_size = len(content)
            
            if file_size > Config.MAX_FILE_SIZE:
                errors.append(f"{file.filename}: File size exceeds maximum limit of {Config.MAX_FILE_SIZE / (1024*1024):.1f}MB")
                continue
            
            # Save file to session directory
            session_path = os.path.join(db_session_manager.upload_dir, session_id)
            os.makedirs(session_path, exist_ok=True)
            file_path = os.path.join(session_path, file.filename)
            
            # Save file content directly (we already have it in memory)
            # This avoids file locking issues on Windows
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # File is now closed, safe to parse
            
            # Parse Excel file
            try:
                dataframes = excel_parser.parse_excel(file_path)
                schema_info = excel_parser.extract_schema_info(dataframes)
                
                # Update session with data in database (handles conflicts internally)
                # Pass file_size to the session manager
                db_session_manager.update_session_data(
                    db=db,
                    session_id=session_id,
                    file_path=file_path,
                    file_size=file_size,
                    dataframes=dataframes,
                    schema_info=schema_info
                )
                
                # Get updated session to see final sheet names (after conflict resolution)
                session_data = db_session_manager.get_session(db, session_id)
                
                # Collect info for response - use original sheet names from this file
                sheets = list(dataframes.keys())
                uploaded_files_info.append(FileUploadInfo(
                    filename=file.filename,
                    sheets=sheets,
                    sheet_count=len(sheets)
                ))
                all_sheets.extend(sheets)
                
                # Update all_schema_info from session (includes all sheets after conflict resolution)
                all_schema_info.update(session_data.schema_info)
                
            except Exception as e:
                # Clean up file on error - ensure file is closed first
                try:
                    if os.path.exists(file_path):
                        # Wait a bit and retry if file is locked (Windows issue)
                        import time
                        time.sleep(0.1)
                        os.remove(file_path)
                except (OSError, PermissionError) as cleanup_error:
                    # File might be locked, log but don't fail the whole request
                    print(f"Warning: Could not delete file {file_path}: {cleanup_error}")
                
                # Rollback database transaction on error
                db.rollback()
                errors.append(f"{file.filename}: Error parsing Excel file - {str(e)}")
        
        except Exception as e:
            errors.append(f"{file.filename if file.filename else 'Unknown file'}: {str(e)}")
    
    # If all files failed, return error
    if len(uploaded_files_info) == 0:
        error_msg = "All files failed to upload. " + "; ".join(errors)
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Build response message
    if len(uploaded_files_info) == 1:
        message = f"File '{uploaded_files_info[0].filename}' uploaded and parsed successfully"
    else:
        message = f"{len(uploaded_files_info)} files uploaded and parsed successfully"
    
    if errors:
        message += f". Warnings: {'; '.join(errors)}"
    
    return UploadResponse(
        session_id=session_id,
        message=message,
        files=uploaded_files_info,
        total_sheets=len(all_sheets),
        all_sheets=all_sheets,
        schema=all_schema_info
    )

