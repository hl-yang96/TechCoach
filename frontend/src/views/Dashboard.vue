<template>
  <div>
    <h1>TechCoach Dashboard</h1>
    <p>Welcome to the AI-powered career coaching platform</p>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div>Interview Prep</div>
          </template>
          <div>Generate personalized interview questions</div>
          <el-button type="primary" @click="$router.push('/interview')">Start</el-button>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div>Resume Optimization</div>
          </template>
          <div>Optimize your resume for target roles</div>
          <el-button type="primary" @click="$router.push('/career')">Start</el-button>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div>Document Upload</div>
          </template>
          <div>Upload your career documents</div>
          <el-button type="primary" @click="$router.push('/upload')">Start</el-button>
        </el-card>
      </el-col>
    </el-row>
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
</style>