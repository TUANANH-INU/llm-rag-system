import { useState, useEffect } from 'react'
import './App.css'
import DocumentUpload from './components/DocumentUpload'
import ChatInterface from './components/ChatInterface'
import SystemStatus from './components/SystemStatus'

function App() {
  const [documents, setDocuments] = useState([])
  const [systemStatus, setSystemStatus] = useState('loading')
  const [activeTab, setActiveTab] = useState('chat')

  useEffect(() => {
    checkSystemStatus()
    const interval = setInterval(checkSystemStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkSystemStatus = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/rag/status`)
      if (response.ok) {
        setSystemStatus('ready')
      } else {
        setSystemStatus('error')
      }
    } catch (error) {
      setSystemStatus('error')
    }
  }

  const handleDocumentAdded = (doc) => {
    setDocuments([...documents, doc])
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 RAG Chatbot</h1>
        <SystemStatus status={systemStatus} />
      </header>

      <div className="app-content">
        <nav className="app-nav">
          <button
            className={`nav-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            className={`nav-btn ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            📁 Documents
          </button>
        </nav>

        <main className="app-main">
          {activeTab === 'chat' && (
            <ChatInterface documents={documents} />
          )}
          {activeTab === 'upload' && (
            <DocumentUpload onDocumentAdded={handleDocumentAdded} />
          )}
        </main>
      </div>
    </div>
  )
}

export default App
