# Finance AI Agent - Backend

FastAPI backend for the Finance AI Agent application.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
  
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL= model being used
   MAX_FILE_SIZE - Maximum file upload size in bytes (default: 10485760 = 10MB)
   SESSION_TIMEOUT_HOURS - Session timeout in hours (default: 24)
   CORS_ORIGINS - Comma-separated allowed origins or * for all (default: *)
   DB_USER=
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=finance_ai_agent
   HOST= server host 
   PORT= server port

   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`
   
   API documentation: `http://localhost:8000/docs`


## Architecture

- **Session-based**: Each session gets a unique session ID
- **File storage**: Uploaded files stored in `uploads/{session_id}/`
- **Multi-sheet support**: Automatically handles Excel files with multiple sheets
- **AI-powered**: Uses Google Gemini for natural language understanding and code generation
- **Safe execution**: Code execution in restricted context

## Multi-Sheet Support

The application fully supports Excel files with multiple sheets:

- **Automatic parsing**: All sheets are parsed and stored separately
- **Intelligent selection**: AI automatically selects the relevant sheet(s) based on your question
- **Cross-sheet queries**: Can combine data from multiple sheets when needed
- **Sheet-aware visualizations**: Charts can be generated from single or multiple sheets

