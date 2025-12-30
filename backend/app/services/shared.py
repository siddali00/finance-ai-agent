"""
Shared service instances used across the application
"""
from app.services.db_session_manager import DBSessionManager
from app.services.excel_parser import ExcelParser
from app.services.gemini_service import GeminiService
from app.services.chart_generator import ChartGenerator
from app.config import Config
import os

# Shared instances - initialized once
db_session_manager = DBSessionManager(upload_dir=Config.UPLOAD_DIR)
excel_parser = ExcelParser()

# Gemini service - will be initialized when API key is available
# Initialize lazily to handle missing API key gracefully
_gemini_service = None

def get_gemini_service():
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        try:
            _gemini_service = GeminiService()
        except ValueError as e:
            # API key not set - will fail when actually used
            pass
    return _gemini_service

chart_generator = ChartGenerator()

