from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class SessionResponse(BaseModel):
    session_id: str


class FileUploadInfo(BaseModel):
    filename: str
    sheets: List[str]
    sheet_count: int

class UploadResponse(BaseModel):
    session_id: str
    message: str
    files: List[FileUploadInfo]
    total_sheets: int
    all_sheets: List[str]
    schema: Dict[str, Any]


class QueryRequest(BaseModel):
    session_id: Optional[str] = None
    question: str


class QueryResponse(BaseModel):
    session_id: str
    answer: str
    query_used: Optional[str] = None
    data: Optional[Any] = None


class VisualizeRequest(BaseModel):
    session_id: Optional[str] = None
    request: str


class VisualizeResponse(BaseModel):
    session_id: str
    chart_type: str
    chart_data: Dict[str, Any]
    description: str

