import axios from 'axios'

// Get base URL from environment or use default
const API_BASE_URL = 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor 
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here later
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor 
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Export the api object for use in components
export default api

// Individual service exports for specific domains
export const healthService = {
  getHealth: () => api.get('/health'),
  getDetailedHealth: () => api.get('/health/detailed')
}

export const documentService = {
  // Ingest documents from file path or text content
  ingestDocument: (data) => {
    return api.post('/api/documents/ingest', data)
  },

  // Get list of uploaded documents
  getDocumentList: () => api.get('/api/documents/list'),

  // Get document collections
  getCollections: () => api.get('/api/documents/collections'),

  // Health check
  getHealth: () => api.get('/api/documents/health'),

  // Legacy upload method (keeping for compatibility)
  uploadDocument: (file, metadata) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('metadata', JSON.stringify(metadata))
    return api.post('/api/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getDocuments: () => api.get('/api/documents'),
  deleteDocument: (id) => api.delete(`/api/documents/${id}`)
}
