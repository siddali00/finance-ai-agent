from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse
from app.services.shared import db_session_manager, get_gemini_service
from app.database import get_db
from sqlalchemy.orm import Session
import os
import pandas as pd
import numpy as np
from typing import Any, Optional

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_data(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Answer a natural language question about the uploaded data
    If session_id is not provided or invalid, a new session will be created
    """
    # Get or create session
    session_id = db_session_manager.get_or_create_session(db, request.session_id)
    
    # Get session data
    try:
        session = db_session_manager.get_session(db, session_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if data is uploaded
    if not session.dataframes:
        raise HTTPException(
            status_code=400,
            detail="No data uploaded for this session. Please upload an Excel file first."
        )
    
    try:
        # Get Gemini service
        gemini_service = get_gemini_service()
        if gemini_service is None:
            raise HTTPException(
                status_code=500,
                detail="Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
            )
        
        # Generate code to answer the question
        code = gemini_service.generate_query_code(
            question=request.question,
            schema_info=session.schema_info
        )
        
        # Execute the code safely
        safe_globals = {
            'pd': __import__('pandas'),
            'dataframes': session.dataframes,
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                '__import__': __import__,
            }
        }
        
        exec(code, safe_globals)
        
        # Get result
        if 'result' in safe_globals:
            result = safe_globals['result']
        else:
            # Try to get the last expression result
            result = None
        
        # Convert result to serializable format
        result_data: Optional[Any] = None
        if result is not None:
            try:
                if isinstance(result, pd.DataFrame):
                    result_data = result.to_dict('records')
                elif isinstance(result, pd.Series):
                    result_data = result.tolist()
                elif isinstance(result, (np.integer, np.floating, np.bool_)):
                    result_data = result.item()  # Convert numpy types to Python native types
                elif isinstance(result, (int, float, str, bool, type(None))):
                    result_data = result
                elif isinstance(result, (list, dict)):
                    result_data = result
                else:
                    result_data = str(result)  # Fallback to string representation
            except Exception as e:
                # If conversion fails, use string representation
                result_data = str(result)
        
        # Generate natural language answer
        answer = gemini_service.generate_answer_from_result(
            question=request.question,
            result=result
        )
        
        # Save conversation to database
        db_session_manager.save_conversation(
            db=db,
            session_id=session_id,
            question=request.question,
            answer=answer,
            query_used=code
        )
        
        return QueryResponse(
            session_id=session_id,
            answer=answer,
            query_used=code,
            data=result_data
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

