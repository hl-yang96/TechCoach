/**
 * Vue.js 3 Application Entry Point
 * File: frontend/src/main.js
 * Created: 2025-07-17
 * Purpose: Vue.js application initialization and configuration
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

// Create Vue app
const app = createApp(App)

// Mount plugins
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)
}

app.mount('#app')