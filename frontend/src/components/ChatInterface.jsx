import { useState, useRef, useEffect } from 'react'
import { ragAPI } from '../services/api'
import './ChatInterface.css'

function ChatInterface({ documents }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [retrievalCount, setRetrievalCount] = useState(5)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!input.trim() || documents.length === 0) {
      if (documents.length === 0) {
        alert('Please upload or load documents first')
      }
      return
    }

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await ragAPI.query(input, retrievalCount)
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        retrievedDocs: response.retrieved_docs
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.message}`,
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-container">
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h2>👋 Welcome to RAG Chatbot</h2>
              <p>Upload or load documents, then ask questions about them!</p>
              <div className="tips">
                <h3>Tips:</h3>
                <ul>
                  <li>Upload PDF documents or load content from websites</li>
                  <li>Ask specific questions about your documents</li>
                  <li>Answers include citations to source documents</li>
                  <li>Adjust retrieval count for more/fewer sources</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}
                >
                  <div className="message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <p className="message-text">{msg.content}</p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="message-sources">
                        <strong>📚 Sources:</strong>
                        <ul>
                          {msg.sources.map((source, i) => (
                            <li key={i}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {msg.confidence !== undefined && (
                      <div className="message-metadata">
                        <span className="confidence">
                          ✓ Confidence: {(msg.confidence * 100).toFixed(0)}%
                        </span>
                        <span className="retrieved">
                          📄 Documents: {msg.retrievedDocs}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant loading">
                  <div className="message-avatar">🤖</div>
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
          )}
        </div>

        <div className="chat-controls">
          <div className="control-group">
            <label htmlFor="retrieval-count">📄 Retrieval Count:</label>
            <input
              id="retrieval-count"
              type="number"
              min="1"
              max="20"
              value={retrievalCount}
              onChange={(e) => setRetrievalCount(parseInt(e.target.value))}
              disabled={loading}
            />
          </div>
        </div>

        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              documents.length === 0
                ? 'Load documents first...'
                : 'Ask a question...'
            }
            disabled={loading || documents.length === 0}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={loading || !input.trim() || documents.length === 0}
            className="send-btn"
          >
            {loading ? '⏳' : '📤'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface
