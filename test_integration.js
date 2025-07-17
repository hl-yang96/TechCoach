// Quick frontend-backend integration test
// Run with: node test_integration.js

const axios = require('axios');

const BASE_URL = 'http://localhost:8001';
const FRONTEND_URL = 'http://localhost:3000';

async function testEndpoints() {
  console.log('🧪 Testing TechCoach Frontend-Backend Integration...\n');
  
  const endpoints = [
    '/health',
    '/health/detailed',
    '/docs',
  ];
  
  for (const endpoint of endpoints) {
    try {
      const response = await axios.get(`${BASE_URL}${endpoint}`, { timeout: 5000 });
      console.log(`✅ ${BASE_URL}${endpoint} - Status: ${response.status}`);
    } catch (error) {
      console.log(`❌ ${BASE_URL}${endpoint} - Error: ${error.message}`);
    }
  }
  
  console.log('\n📋 Integration Checklist:');
  console.log('1. Backend running: http://localhost:8001');
  console.log('2. Frontend running: http://localhost:3000');
  console.log('3. Proxy working: http://localhost:3000/api/health');
  console.log('4. CORS configured for http://localhost:3000');
  
  console.log('\n🚀 Quick Start Commands:');
  console.log('Terminal 1: uvicorn app.main:app --reload --port 8001');
  console.log('Terminal 2: cd frontend && npm run dev');
  console.log('Browser: http://localhost:3000');
}

testEndpoints().catch(console.error);