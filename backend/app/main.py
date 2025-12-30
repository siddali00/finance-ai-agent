from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, upload, query, visualize
from app.config import Config
from app.database import init_db

app = FastAPI(
    title="Finance AI Agent API",
    description="AI-powered financial data analysis and visualization",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

# CORS middleware - configured from environment variables
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(session.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(visualize.router)


@app.get("/")
async def root():
    return {
        "message": "Finance AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "session": "/api/session",
            "upload": "/api/upload",
            "query": "/api/query",
            "visualize": "/api/visualize"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

