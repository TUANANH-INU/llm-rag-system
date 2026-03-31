import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 120000, // 2 minutes for LLM generation
})

// Document APIs
export const documentAPI = {
  uploadPDF: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/documents/upload-pdf/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  loadURL: async (url) => {
    const response = await api.post('/api/documents/load-url/', { url })
    return response.data
  },

  listDocuments: async () => {
    const response = await api.get('/api/documents/list/')
    return response.data
  },

  deleteDocument: async (documentId) => {
    const response = await api.delete(`/api/documents/delete/${documentId}`)
    return response.data
  },
}

// RAG APIs
export const ragAPI = {
  query: async (question, k = 5) => {
    const response = await api.post('/api/rag/query', {
      question,
      k
    })
    return response.data
  },

  addPDF: async (pdfPath) => {
    const response = await api.post('/api/rag/add-pdf', null, {
      params: { pdf_path: pdfPath }
    })
    return response.data
  },

  addURL: async (url) => {
    const response = await api.post('/api/rag/add-url', null, {
      params: { url }
    })
    return response.data
  },

  saveVectorStore: async (path = 'data/vector_store') => {
    const response = await api.post('/api/rag/save', null, {
      params: { path }
    })
    return response.data
  },

  loadVectorStore: async (path = 'data/vector_store') => {
    const response = await api.post('/api/rag/load', null, {
      params: { path }
    })
    return response.data
  },

  getStatus: async () => {
    const response = await api.get('/api/rag/status')
    return response.data
  },
}

export default api
