<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <el-header style="background: #001529; color: white; display: flex; align-items: center; padding: 0 20px;">
        <div style="font-size: 1.5em; font-weight: bold; margin-right: 40px;">TechCoach</div>
        <div style="display: flex; align-items: center; flex: 1;">
          <el-menu
            mode="horizontal"
            background-color="#001529"
            text-color="#fff"
            active-text-color="#ffd04b"
            :router="true"
            :default-active="$route.path"
            style="border-bottom: none;"
          >
            <el-menu-item index="/">Dashboard</el-menu-item>
            <el-menu-item index="/interview">Interview Prep</el-menu-item>
            <el-menu-item index="/upload">Documents</el-menu-item>
            <el-menu-item index="/career">Career</el-menu-item>
          </el-menu>
          
          <!-- Health Check Component -->
          <NavigationHealth />
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer style="text-align: center; background: #f0f2f5;">
        TechCoach © 2025 - AI-Powered Career Coaching Platform
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
  margin: 0;
  padding: 0;
}

.el-header .el-menu--horizontal {
  border-bottom: none;
  margin-left: 40px;
}
</style>