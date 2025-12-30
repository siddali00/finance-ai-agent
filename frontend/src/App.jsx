import { useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import apiService from './services/api';
import './App.css';

function App() {
  useEffect(() => {
    // Reset session on page load (new session will be created on first API call)
    apiService.resetSession();
  }, []);

  return (
    <div className="App">
      <ChatWindow />
      </div>
  );
}

export default App;
