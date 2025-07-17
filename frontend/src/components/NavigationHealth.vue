<template>
  <div class="nav-health-indicator">
    <div v-if="loading" class="health-loading">
      <div class="health-spinner"></div>
      <span>Connecting...</span>
    </div>
    
    <div v-else-if="error" class="health-error" :title="error">
      <el-icon><Warning /></el-icon>
      <span class="health-text">Offline</span>
    </div>
    
    <div v-else-if="apiStatus" class="health-ok" :title="`Backend: ${apiStatus.status} | Version: ${apiStatus.version}`">
      <el-icon class="health-icon">
        <Monitor />
      </el-icon>
      <span class="health-text">Online</span>
      
      <!-- Services popup on hover -->
      <div class="health-popup">
        <div class="popup-title">Backend Status</div>
        <div class="service-item" v-for="(status, service) in apiStatus.services" :key="service">
          <span class="service-name">{{ service }}:</span>
          <span :class="status === 'healthy' ? 'status-ok' : 'status-error'">
            {{ status }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api.js'
import { Monitor, Warning } from '@element-plus/icons-vue'

export default {
  name: 'NavigationHealth',
  components: {
    Monitor,
    Warning
  },
  data() {
    return {
      apiStatus: null,
      loading: false,
      error: null,
      retryCount: 0,
      maxRetries: 3
    }
  },
  mounted() {
    this.testAPI();
    // Re-test every 30 seconds
    this.healthCheckInterval = setInterval(() => {
      this.testAPI();
    }, 30000);
  },
  beforeUnmount() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }
  },
  methods: {
    async testAPI() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.get('/health');
        this.apiStatus = response.data;
        this.error = null;
        this.retryCount = 0;
        
      } catch (err) {
        this.error = `Failed to connect: ${err.message}`;
        this.apiStatus = null;
        this.retryCount++;
        
        // Retry with backoff
        if (this.retryCount < this.maxRetries) {
          setTimeout(() => this.testAPI(), this.retryCount * 1000);
        }
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.nav-health-indicator {
  margin-left: auto;
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.health-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e6a23c;
  font-size: 0.9em;
}

.health-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e6a23c;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.health-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #f56c6c;
  cursor: pointer;
}

.health-ok {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #67c23a;
  cursor: pointer;
  position: relative;
}

.health-icon {
  font-size: 18px;
}

.health-text {
  font-size: 0.9em;
  font-weight: 500;
}

.health-ok:hover .health-popup {
  display: block;
}

.health-popup {
  display: none;
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 8px;
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 1000;
}

.popup-title {
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.service-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.9em;
}

.service-name {
  color: #606266;
}

.status-ok {
  color: #67c23a;
}

.status-error {
  color: #f56c6c;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>