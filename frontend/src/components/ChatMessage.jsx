import { useEffect, useRef } from 'react';
import Plot from 'react-plotly.js';

const ChatMessage = ({ message, isUser }) => {
  const messageRef = useRef(null);

  useEffect(() => {
    if (messageRef.current) {
      messageRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [message]);

  if (isUser) {
    return (
      <div ref={messageRef} className="message user-message">
        <div className="message-content">
          <p>{message.text}</p>
        </div>
      </div>
    );
  }

  return (
    <div ref={messageRef} className="message ai-message">
      <div className="message-content">
        {message.type === 'text' && (
          <div>
            <p className="answer-text">{message.text}</p>
          </div>
        )}
        
        {message.type === 'chart' && message.chartData && (
          <div className="chart-container">
            <Plot
              data={message.chartData.data}
              layout={message.chartData.layout || {}}
              config={{ displayModeBar: true, responsive: true }}
              style={{ width: '100%', height: '400px' }}
            />
            <p className="chart-description">{message.description}</p>
          </div>
        )}

        {message.type === 'error' && (
          <div className="error-message">
            <p>❌ {message.text}</p>
          </div>
        )}

        {message.type === 'upload' && (
          <div className="upload-success">
            <p>✅ {message.text}</p>
            {message.files && (
              <ul className="uploaded-files-list">
                {message.files.map((file, idx) => (
                  <li key={idx}>
                    <strong>{file.filename}</strong> - {file.sheet_count} sheet(s)
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;

