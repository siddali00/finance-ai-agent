# Finance AI Agent - Frontend

Modern React frontend for the Finance AI Agent application.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API URL :**
   ```
   VITE_API_URL= the backend url
   ```

3. **Start development server:**
   ```
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

4. **Build for production:**
   ```bash
   npm run build
   ```

## Usage

1. **Upload Files:**
   - Drag and drop Excel files onto the upload area
   - Or click to select files
   - Multiple files supported

2. **Ask Questions:**
   - Once files are uploaded, type your question
   - Examples:
     - "What was the total sales for Q3?"
     - "Which branch had the highest revenue?"
     - "Show me a bar chart of sales by branch"

3. **View Visualizations:**
   - Ask for charts/graphs
   - Interactive Plotly charts will be displayed

## Architecture

- **Session Management:** Session ID is automatically generated and stored
- **State Management:** React hooks (useState, useEffect)
- **API Service:** Centralized API calls with axios
- **Components:**
  - `ChatWindow` - Main chat interface
  - `ChatMessage` - Individual message display
  - `FileUpload` - File upload component

