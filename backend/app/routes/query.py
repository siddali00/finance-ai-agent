from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse
from app.services.shared import db_session_manager, get_gemini_service
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_data(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Answer a natural language question - handles greetings, data queries, and out-of-scope questions
    If session_id is not provided or invalid, a new session will be created
    """
    # Get or create session
    session_id = db_session_manager.get_or_create_session(db, request.session_id)
    
    # Get session data
    try:
        session = db_session_manager.get_session(db, session_id)
        has_data = bool(session.dataframes)
        schema_info = session.schema_info if has_data else {}
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Please upload files first."
        )
    
    # Require files to be uploaded before any conversation
    if not has_data:
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
        
        # Classify the query using AI
        query_type = gemini_service.classify_query(
            question=request.question,
            has_data=has_data,
            schema_info=schema_info if has_data else None
        )
        
        # Handle different query types
        if query_type == 'greeting' or query_type == 'conversational':
            # Handle greetings and conversational queries
            answer = gemini_service.handle_conversational_query(
                question=request.question,
                has_data=has_data,
                schema_info=schema_info if has_data else None
            )
            
            # Save conversation
            db_session_manager.save_conversation(
                db=db,
                session_id=session_id,
                question=request.question,
                answer=answer,
                query_used=None
            )
            
            return QueryResponse(
                session_id=session_id,
                answer=answer,
                query_used=None,
                data=None
            )
        
        elif query_type == 'out_of_scope':
            # Politely decline
            answer = gemini_service.handle_out_of_scope_query(request.question)
            
            # Save conversation
            db_session_manager.save_conversation(
                db=db,
                session_id=session_id,
                question=request.question,
                answer=answer,
                query_used=None
            )
            
            return QueryResponse(
                session_id=session_id,
                answer=answer,
                query_used=None,
                data=None
            )
        
        elif query_type == 'data_query':
            # Process data query (data is guaranteed to exist due to check above)
            # Generate code to answer the question
            code = gemini_service.generate_query_code(
                question=request.question,
                schema_info=schema_info
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
                result = None
            
            # Generate natural language answer
            answer = gemini_service.generate_answer_from_result(
                question=request.question,
                result=result
            )
            
            # Save conversation (code is saved but not shown to user)
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
                query_used=None,  # Don't send code to frontend
                data=None  # Data not used by frontend, only AI answer is displayed
            )
        
        else:
            # Fallback to conversational
            answer = gemini_service.handle_conversational_query(
                question=request.question,
                has_data=has_data,
                schema_info=schema_info if has_data else None
            )
            
            db_session_manager.save_conversation(
                db=db,
                session_id=session_id,
                question=request.question,
                answer=answer,
                query_used=None
            )
            
            return QueryResponse(
                session_id=session_id,
                answer=answer,
                query_used=None,
                data=None
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

