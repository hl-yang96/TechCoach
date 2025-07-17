<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold text-gray-900">TechCoach Dashboard</h1>
      <p class="text-gray-600 mt-2">AI-powered career coaching platform</p>
      
      <!-- Main Features -->
      <el-row :gutter="20" class="mt-6">
        <el-col :span="8">
          <el-card>
            <template #header>
              <div>Interview Prep</div>
            </template>
            <div>Generate personalized interview questions</div>
            <el-button type="primary" @click="$router.push('/interview')" class="mt-2">Start</el-button>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card>
            <template #header>
              <div>Resume Optimization</div>
            </template>
            <div>Optimize your resume for target roles</div>
            <el-button type="primary" @click="$router.push('/career')" class="mt-2">Start</el-button>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card>
            <template #header>
              <div>Document Upload</div>
            </template>
            <div>Upload your career documents</div>
            <el-button type="primary" @click="$router.push('/upload')" class="mt-2">Start</el-button>
          </el-card>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
}
</script>

<style scoped>
.el-card {
  height: 200px;
}

.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>