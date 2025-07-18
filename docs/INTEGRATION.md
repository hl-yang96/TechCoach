# Frontend ↔ Backend Integration Guide

This guide explains how to integrate the TechCoach Frontend (Vue.js) with the Backend (FastAPI) in detail.

## 🔗 Architecture Overview

```
Frontend (Vue.js)          Backend (FastAPI)
┌─────────────────┐        ┌─────────────────┐
│   localhost:3000│  <───> │   localhost:8001│
│   Development   │        │     API Server   │
│   Server        │        │                  │
└─────────────────┘        └─────────────────┘
        │                           │
        └───/api/* proxy─────────────┘
```

## 🚀 Complete Integration Steps

### Step 1: Environment Setup

#### ⚙️ Set Environment Variables

Create `.env` files in both frontend and backend:

**Backend `.env` (in project root):**
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
CHROMA_HOST=localhost
CHROMA_PORT=8000
DB_PATH=./app_data/sqlite.db
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Frontend `.env.local` (in frontend folder):**
```bash
VITE_API_BASE_URL=http://localhost:8001/api
VITE_APP_NAME=TechCoach
```

#### 🏗️ Start Backend First

1. **Install Python dependencies** (if not done):
   ```bash
   cd /Users/hlyang/hlyang_workspace/project/personal/TechCoach/
   pip install -r requirements.txt
   ```

2. **Start the FastAPI backend** in a terminal:
   ```bash
   uvicorn app.main:app --reload --port 8001 --log-level info
   ```
   
   You should see: 
   ```
   🚀 TechCoach API started successfully!
   INFO:     Uvicorn running on http://127.0.0.1:8001
   ```

3. **Test backend health**:
   Open browser → http://localhost:8001/health
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-07-17T16:00:00.000Z",
     "version": "0.1.0",
     "services": { "api": "healthy", "database": "healthy", "vector_db": "healthy" }
   }
   ```

#### 🎨 Start Frontend Second

4. **In another terminal, start frontend:**
   ```bash
   cd frontend
   npm install  # If not done already
   npm run dev
   ```
   
   Should show: `Local: http://localhost:3000/`

### Step 2: Proxy Configuration (Already Setup)

#### ✨ How Proxy Works
- **Frontend port**: 3000
- **Backend port**: 8001
- **Proxy rule**: `/api/*` → `http://localhost:8001/api/*`

```javascript
// In frontend/vite.config.js
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8001',  // Backend URL
      changeOrigin: true,               // Handle CORS
      secure: false                    // Use HTTP
    }
  }
}
```

#### ✅ Check Proxy Configuration

5. **Test proxy**: Open browser → http://localhost:3000/api/health
   
   Should redirect through proxy and show the same API response.

### Step 3: Create API Service Layer

#### 📦 Create API Service (if not exists)

6. **Create `frontend/src/services/api.js`:**
   ```javascript
   import axios from 'axios'

   const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'

   const api = axios.create({
     baseURL: API_BASE_URL,
     timeout: 30000,
     headers: {
       'Content-Type': 'application/json',
     },
   })

   // Request interceptor (for auth tokens - future use)
   api.interceptors.request.use(
     (config) => {
       // Add auth token here when you implement authentication
       return config
     },
     (error) => {
       return Promise.reject(error)
     }
   )

   // Response interceptor (for error handling)
   api.interceptors.response.use(
     (response) => response,
     (error) => {
       console.error('API Error:', error.response?.data || error.message)
       return Promise.reject(error)
     }
   )

   export default api
   ```

### Step 4: Test API Integration

#### 🧪 Integration Testing

7. **Update Dashboard.vue to test connection:**
   ```vue
   <template>
     <div class="max-w-7xl mx-auto px-4 py-8">
       <div class="bg-white rounded-lg shadow p-6">
         <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
         
         <div class="mt-6 space-y-4">
           <div class="border rounded-lg p-4">
             <h3 class="font-semibold mb-2">API Status:</h3>
             <div v-if="apiStatus" class="text-sm">
               <p><strong>Status:</strong> {{ apiStatus.status }}</p>
               <p><strong>Version:</strong> {{ apiStatus.version }}</p>
               <p><strong>Timestamp:</strong> {{ apiStatus.timestamp }}</p>
             </div>
             <div v-else class="text-gray-500">
               Loading API status...
             </div>
           </div>

           <button 
             @click="testAPI" 
             class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
             :disabled="loading"
           >
             {{ loading ? 'Testing...' : 'Test API Connection' }}
           </button>

           <div v-if="error" class="text-red-500">
             Error: {{ error }}
           </div>
         </div>
       </div>
     </div>
   </template>

   <script>
   import api from '@/services/api.js'

   export default {
     name: 'Dashboard',
     data() {
       return {
         apiStatus: null,
         loading: false,
         error: null
       }
     },
     async mounted() {
       await this.testAPI()
     },
     methods: {
       async testAPI() {
         this.loading = true
         this.error = null
         
         try {
           const response = await api.get('/health')
           this.apiStatus = response.data
         } catch (err) {
           this.error = err.message
         } finally {
           this.loading = false
         }
       }
     }
   }
   </script>
   ```

### Step 5: Environment Validation Checklist

#### ✅ Quick Validation Commands

Run these commands to verify your setup:

```bash
# 1. Backend health check
curl http://localhost:8001/health

# 2. Frontend dev server check
curl http://localhost:3000

# 3. API proxy check
curl http://localhost:3000/api/health

# 4. Backend detailed check
curl http://localhost:8001/health/detailed

# 5. Backend endpoints list
curl http://localhost:8001/docs  # Opens Swagger UI
```

### Step 6: Docker Integration (Optional)

If you want to use Docker for full-stack development:

```bash
docker-compose up --build
```

This automatically sets up:
- Backend on :8001
- Frontend on :3000
- ChromaDB on :8000

#### 🐳 Docker-Based URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- API within Docker containers use service names:
  - Frontend → http://backend:8001/api
  - Backend → http://chroma:8000

### Step 7: Debug Common Issues

#### 🔍 Connection Troubleshooting

**Problem: "Network Error" in browser**

1. **Check if backend is running:**
   ```bash
   # Should return health data
   curl http://localhost:8001/health
   ```

2. **Check proxy configuration:**
   ```bash
   # Should redirect to backend
   curl http://localhost:3000/api/health
   ```

3. **Check CORS settings** (in app/main.py):
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

**Problem: "CORS Failed"**
- Backend might not have CORS enabled for localhost:3000
- Solution: Check .env file has proper ALLOWED_ORIGINS

**Problem: "Port already in use"**
```bash
# Kill processes on ports 3000/8001
lsof -ti:3000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

### Step 8: Complete API Endpoints

Here are the available endpoints you can use:

| Endpoint | Method | Returns | Description |
|----------|--------|---------|-------------|
| `/api/health` | GET | Status JSON | Basic health check |
| `/api/health/detailed` | GET | Detailed status | Service level health |
| `/api/health/ready` | GET | {"status": "ready"} | Kubernetes readiness |
| `/api/health/live` | GET | {"status": "alive"} | Kubernetes liveness |

Access the interactive documentation: http://localhost:8001/docs

### ✅ Success Test

When everything works, you should see:

1. **Backend**: http://localhost:8001/health shows JSON
2. **Frontend**: http://localhost:3000 shows the Vue app
3. **Integration**: Your Dashboard displays API status automatically
4. **Docs**: http://localhost:8001/docs shows all available endpoints

### 🎥 Next Steps After Integration

1. **Create service modules** for each domain
2. **Add loading states** with Vue components
3. **Implement error handling** with user-friendly messages
4. **Add real endpoints** for your actual features

----

**🎯 TL;DR Quick Start:**

```bash
# Terminal 1: Backend
uvicorn app.main:app --reload --port 8001

# Terminal 2: Frontend  
cd frontend && npm run dev

# Browser: http://localhost:3000/api/health
# Should work immediately!
```