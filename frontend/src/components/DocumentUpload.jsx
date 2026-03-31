import { useState } from 'react'
import { documentAPI, ragAPI } from '../services/api'
import './DocumentUpload.css'

function DocumentUpload({ onDocumentAdded }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [uploadMode, setUploadMode] = useState('pdf')
  const [url, setUrl] = useState('')
  const [documents, setDocuments] = useState([])

  const handlePDFUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await documentAPI.uploadPDF(file)
      setSuccess(`PDF uploaded: ${result.name}`)
      
      // Add to RAG system
      await ragAPI.addPDF(result.source)
      onDocumentAdded(result)
      
      // Refresh document list
      const docs = await documentAPI.listDocuments()
      setDocuments(docs.documents)
      
      e.target.value = ''
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleURLSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim()) {
      setError('Please enter a valid URL')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await documentAPI.loadURL(url)
      setSuccess(`URL loaded: ${result.name}`)
      
      // Add to RAG system
      await ragAPI.addURL(url)
      onDocumentAdded(result)
      
      setUrl('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load URL')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (docName) => {
    try {
      await documentAPI.deleteDocument(docName)
      const docs = await documentAPI.listDocuments()
      setDocuments(docs.documents)
      setSuccess(`Document deleted: ${docName}`)
    } catch (err) {
      setError('Failed to delete document')
    }
  }

  return (
    <div className="document-upload">
      <div className="upload-section">
        <h2>📚 Document Management</h2>
        
        <div className="upload-mode">
          <button
            className={`mode-btn ${uploadMode === 'pdf' ? 'active' : ''}`}
            onClick={() => setUploadMode('pdf')}
          >
            📄 Upload PDF
          </button>
          <button
            className={`mode-btn ${uploadMode === 'url' ? 'active' : ''}`}
            onClick={() => setUploadMode('url')}
          >
            🌐 Load URL
          </button>
        </div>

        {uploadMode === 'pdf' && (
          <div className="upload-form">
            <label htmlFor="pdf-input" className="file-input-label">
              {loading ? 'Uploading...' : 'Click to select PDF or drag file here'}
            </label>
            <input
              id="pdf-input"
              type="file"
              accept=".pdf"
              onChange={handlePDFUpload}
              disabled={loading}
              className="file-input"
            />
          </div>
        )}

        {uploadMode === 'url' && (
          <form onSubmit={handleURLSubmit} className="url-form">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter website URL (https://example.com)"
              disabled={loading}
              className="url-input"
            />
            <button
              type="submit"
              disabled={loading || !url.trim()}
              className="submit-btn"
            >
              {loading ? 'Loading...' : 'Load Website'}
            </button>
          </form>
        )}

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}
      </div>

      <div className="documents-list">
        <h3>📖 Uploaded Documents</h3>
        {documents.length === 0 ? (
          <p className="empty-message">No documents uploaded yet</p>
        ) : (
          <div className="docs-grid">
            {documents.map((doc, idx) => (
              <div key={idx} className="doc-card">
                <div className="doc-info">
                  <h4>{doc.name}</h4>
                  <p>{(doc.size / 1024).toFixed(2)} KB</p>
                </div>
                <button
                  onClick={() => handleDelete(doc.name)}
                  className="delete-btn"
                  title="Delete document"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentUpload
