# Finance AI Agent

A natural language interface for analyzing Excel data using AI. Upload your Excel files, ask questions in plain English, and get answers with visualizations.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL database
- Google Gemini API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate ## on MACOS, LINUX 
   venv\Scripts\activate  ## On Windows:
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=finance_ai_agent
   MAX_FILE_SIZE=10485760
   HOST=0.0.0.0
   PORT=8000
   CORS_ORIGINS=*
   ```

4. **Initialize database:**
   ```bash
   python init_db.py
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   API available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API URL:**
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_URL=http://localhost:8000 
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```
   
   App available at `http://localhost:5173`

## Architecture Overview

### Key Technologies

- **Backend and Database**: FastAPI
- **Frontend**: React, Vite, Axios, Plotly.js
- **AI**: Gemini
- **Database**: PostgreSQL

### Data Flow

1. User uploads Excel files → Stored on disk, parsed into DataFrames
2. User asks question → AI generates pandas code
3. Code executes in sandbox → Result obtained
4. AI generates natural language answer → Sent to frontend
5. For visualizations → AI generates Plotly code → sent to frontend

## Assumptions and Design Decisions

### Assumptions

1. **File Format**: Only `.xlsx` and `.xls` Excel files are supported
2. **File Size**: Maximum file size limit (default 10MB) to prevent memory issues
3. **Session Persistence**: Files must remain on disk for sessions to persist across server restarts
4. **Single Server**: Designed for single instance deployment (local file storage)
5. **Trusted Environment**: Code execution sandbox assumes trusted AI generated code

### Design Decisions

1. **Database vs File Storage**
   - **Metadata in DB**: Session info, file paths, schema info stored in PostgreSQL
   - **Files on Disk**: Excel files stored locally (not in DB) for performance
   - **DataFrames in Memory**: Cached in memory, reloaded from files on demand

2. **Session Management**
   - **Auto-creation**: Sessions auto created if not provided or invalid
   - **UUID-based**: Each session gets unique UUID for identification

3. **Code Execution**
   - **Sandboxed**: Restricted environment with only safe functions
   - **No Serialization**: Results sent directly to AI, not serialized for frontend
   - **AI-Powered**: All code generation handled by Gemini AI

4. **Error Handling**
   - **Graceful Degradation**: Falls back to conversational responses on errors
   - **User Friendly**: Technical errors converted to friendly messages
   - **Validation**: File type and size validated before processing

5. **Frontend Simplicity**
   - **No State Management Library**: Uses React hooks only
   - **No Code Display**: Generated code hidden from users
   - **Conversational UI**: Chat-based interface for natural interaction

## What Would I Improve With More Time?

### 1. **Scalability**
   - **S3 Storage**: Move file storage to S3
   - **Redis Cache**: Add Redis for distributed DataFrame caching

### 2. **Security**
   - **Enhanced Sandbox**: More restrictive code execution environment
   - **Rate Limiting**: Prevent abuse of API endpoints
   - **Authentication**: User authentication and authorization
   - **Input Validation**: More robust validation of AI generated code

### 3. **Performance**
   - **Async File Processing**: Process large files asynchronously

### 4. **Features**
   - **Data Export**: Allow users to export analysis results
   - **Query History**: Better query history and search ( CONTEXT OF PREVIOUS MESSAGES)
   - **Multiple Users**: Support multiple users with data isolation
   - **File Management**: UI to view/delete uploaded files

### 5. **Code Quality**
   - **Testing**: Comprehensive unit and integration tests
   - **Error Logging**: Structured logging with error tracking (Sentry)

### 6. **User Experience**
   - **Progress Indicators**: Show progress for long running queries
   - **Query Suggestions**: Suggest related queries
   - **Data Preview**: Show data preview before analysis

### 7. **Monitoring & Observability**
   - **Metrics**: Track API usage, response times, errors

## Project Structure

```
assessment/
├── backend/
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models/        # Database & API models
│   │   └── main.py        # FastAPI app
│   ├── uploads/           # Uploaded Excel files
│   ├── requirements.txt
│   └── init_db.py        # Database initialization
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── services/     # API service
│   └── package.json
└── README.md
```

