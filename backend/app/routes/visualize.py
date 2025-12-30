from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import VisualizeRequest, VisualizeResponse
from app.services.shared import db_session_manager, get_gemini_service, chart_generator
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["visualize"])


@router.post("/visualize", response_model=VisualizeResponse)
async def visualize_data(request: VisualizeRequest, db: Session = Depends(get_db)):
    """
    Generate a visualization based on natural language request
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
        
        # Generate chart code
        code = gemini_service.generate_chart_code(
            request=request.request,
            schema_info=session.schema_info
        )
        
        # Execute code and get chart JSON
        chart_data = chart_generator.execute_chart_code(
            code=code,
            dataframes=session.dataframes
        )
        
        # Determine chart type
        chart_type = chart_generator.get_chart_type(chart_data)
        
        # Generate description
        description = f"Visualization showing: {request.request}"
        
        return VisualizeResponse(
            session_id=session_id,
            chart_type=chart_type,
            chart_data=chart_data,
            description=description
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating visualization: {str(e)}"
        )

