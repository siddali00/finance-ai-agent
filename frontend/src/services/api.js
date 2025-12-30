import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

class ApiService {
  constructor() {
    this.sessionId = null;
  }

  // Get or create session
  async getSession() {
    if (!this.sessionId) {
      try {
        const response = await api.get('/api/session');
        this.sessionId = response.data.session_id;
        return this.sessionId;
      } catch (error) {
        console.error('Error creating session:', error);
        throw error;
      }
    }
    return this.sessionId;
  }

  // Upload files
  async uploadFiles(files) {
    const sessionId = await this.getSession();
    
    const formData = new FormData();
    formData.append('session_id', sessionId);
    
    // Add all files
    for (const file of files) {
      formData.append('file', file);
    }

    try {
      const response = await api.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Update session ID if returned
      if (response.data.session_id) {
        this.sessionId = response.data.session_id;
      }
      
      return response.data;
    } catch (error) {
      console.error('Error uploading files:', error);
      throw error;
    }
  }

  // Query data
  async query(question) {
    const sessionId = await this.getSession();
    
    try {
      const response = await api.post('/api/query', {
        session_id: sessionId,
        question: question,
      });
      
      // Update session ID if returned
      if (response.data.session_id) {
        this.sessionId = response.data.session_id;
      }
      
      return response.data;
    } catch (error) {
      console.error('Error querying:', error);
      throw error;
    }
  }

  // Generate visualization
  async visualize(request) {
    const sessionId = await this.getSession();
    
    try {
      const response = await api.post('/api/visualize', {
        session_id: sessionId,
        request: request,
      });
      
      // Update session ID if returned
      if (response.data.session_id) {
        this.sessionId = response.data.session_id;
      }
      
      return response.data;
    } catch (error) {
      console.error('Error generating visualization:', error);
      throw error;
    }
  }

  // Reset session (on page refresh, this will be called)
  resetSession() {
    this.sessionId = null;
  }
}

export default new ApiService();

