import { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import FileUpload from './FileUpload';
import apiService from '../services/api';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasUploadedFiles, setHasUploadedFiles] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Initialize with welcome message
    setMessages([{
      id: Date.now(),
      type: 'text',
      text: '👋 Welcome! Upload your Excel files to get started. I can help you analyze your data and create visualizations.',
      isUser: false,
    }]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleUploadSuccess = (response) => {
    setHasUploadedFiles(true);
    const message = {
      id: Date.now(),
      type: 'upload',
      text: response.message,
      files: response.files,
      isUser: false,
    };
    setMessages(prev => [...prev, message]);
  };

  const handleUploadError = (error) => {
    const message = {
      id: Date.now(),
      type: 'error',
      text: error || 'Failed to upload files. Please try again.',
      isUser: false,
    };
    setMessages(prev => [...prev, message]);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) return;

    if (!hasUploadedFiles) {
      const message = {
        id: Date.now(),
        type: 'error',
        text: 'Please upload Excel files first before asking questions.',
        isUser: false,
      };
      setMessages(prev => [...prev, message]);
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'text',
      text: inputValue,
      isUser: true,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Always call query endpoint - AI will classify and handle visualization requests
      const response = await apiService.query(inputValue);
      
      // Check if response contains chart data (visualization)
      if (response.data && response.data.is_visualization && response.data.chart_data) {
        // It's a visualization - render chart
        const aiMessage = {
          id: Date.now(),
          type: 'chart',
          text: response.answer,
          chartData: response.data.chart_data,
          description: response.answer,
          isUser: false,
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        // It's a text response
        const aiMessage = {
          id: Date.now(),
          type: 'text',
          text: response.answer,
          isUser: false,
        };
        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        type: 'error',
        text: error.response?.data?.detail || error.message || 'An error occurred. Please try again.',
        isUser: false,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h1>💼 Finance AI Agent</h1>
        <p>Ask questions about your financial data</p>
      </div>

      <div className="chat-container" ref={chatContainerRef}>
        <div className="messages-list">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} isUser={message.isUser} />
          ))}
          {isLoading && (
            <div className="message ai-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {!hasUploadedFiles && (
          <div className="upload-section">
            <FileUpload
              onUploadSuccess={handleUploadSuccess}
              onUploadError={handleUploadError}
            />
          </div>
        )}

        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={hasUploadedFiles ? "Ask a question about your data..." : "Upload files first..."}
            disabled={!hasUploadedFiles || isLoading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={!hasUploadedFiles || isLoading || !inputValue.trim()}
            className="send-button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;

