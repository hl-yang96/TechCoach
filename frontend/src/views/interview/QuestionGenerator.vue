<template>
  <div class="question-generator-v2">
    <!-- Sidebar Toggle Button -->
    <button 
      class="sidebar-toggle" 
      @click="toggleSidebar"
      :class="{ collapsed: sidebarCollapsed }"
    >
      <el-icon>
        <ChevronLeft v-if="!sidebarCollapsed" />
        <ChevronRight v-else />
      </el-icon>
    </button>

    <!-- Collapsible Sidebar -->
    <aside 
      class="sidebar" 
      :class="{ collapsed: sidebarCollapsed }"
    >
      <div class="sidebar-header">
        <h3>技术领域</h3>
        <span class="selected-count">({{ selectedCategories.length }})</span>
        <div class="sidebar-actions">
          <el-button 
            type="primary" 
            size="small" 
            @click="toggleAdjustment"
            :icon="Setting"
            text>调整分类</el-button>
        </div>
      </div>

      <div class="sidebar-content">
        <div class="categories-list">
          <div
            v-for="category in availableCategories" 
            :key="category.id"
            class="category-slot"
            :class="{ 
              selected: selectedCategories.includes(category.id),
              disabled: loading
            }"
            @click="toggleCategory(category.id)"
          >
            <div class="category-item-content">
              <div class="category-content">
                <div class="category-name">{{ category.name }}</div>
                <div class="category-description">{{ category.description }}</div>
              </div>
              <el-button
                type="text"
                size="small"
                :icon="Delete"
                circle
                class="delete-category-btn"
                @click.stop="deleteCategory(category.id)"
                v-if="showDeleteButton(category)"
              />
            </div>
          </div>

          <!-- Inline Category Input -->
          <div
            class="add-manual category-slot"
            :class="{ disabled: loading }"
          >
            <div class="category-content add-category-content">
              <el-button
                type="text"
                size="small"
                @click="addInlineCategory"
                :disabled="!inlineCategoryName"
                :icon="Plus"
                circle
              />
              <el-input
                v-model="inlineCategoryName"
                placeholder="添加技术领域..."
                size="small"
                class="inline-category-input"
                @keyup.enter="addInlineCategory"
                maxlength="20"
                show-word-limit
              />
            </div>
          </div>

          <!-- Generate More Button (styled as category) -->
          <div
            class="generate-more category-slot"
            :class="{ disabled: loading }"
            @click="generateMoreCategories"
          >
            <div class="category-content">
              <div class="category-name category-name-center">智能扩展</div>
              <div class="category-description category-description-small">基于 AI + 个人知识图谱</div>
              <div class="category-description category-description-small">生成适合你的背景的技术领域</div>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      

      <!-- Step 1: Category Selection -->
      <div v-if="currentStep === 1" class="step-container">
        <div class="empty-guide" v-if="selectedCategories.length === 0">
          <el-icon size="64"><List /></el-icon>
          <h4>请选择技术大类</h4>
          <p>点击左侧类别进行选择，我将为您生成个性化面试题。</p>
        </div>
        
        <div v-else class="selection-summary">
          <h3>已选择 ({{ selectedCategories.length }}) 个大类</h3>
          <div class="selected-tags">
            <el-tag
              v-for="categoryId in selectedCategories"
              :key="categoryId"
              :closable="true"
              @close="toggleCategory(categoryId)"
              size="small"
            >
              {{ getCategoryName(categoryId) }}
            </el-tag>
          </div>
        </div>
      </div>

      <!-- Step 2: Question Display -->
      <div v-else class="questions-container">
        <div v-if="generatedQuestions.length === 0" class="loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          <p>正在生成面试题...</p>
        </div>

        <div v-else>
          <div class="generation-summary">
            <span class="summary-text">
              <el-icon><CircleCheck /></el-icon>
              已为{{ selectedCategories.length }}个类别生成{{ generatedQuestions.length }}道面试题
            </span>
            <el-button text type="primary" @click="resetAll">重新生成</el-button>
          </div>

          <div class="questions-grid">
            <div 
              v-for="(group, categoryId) in questionsByCategory" 
              :key="categoryId"
              class="category-section"
            >
              <div class="category-header">
                <h3>{{ getCategoryName(categoryId) }}</h3>
                <span class="count">({{ group.length }}题)</span>
              </div>
              
              <el-collapse>
                <el-collapse-item 
                  v-for="(question, index) in group" 
                  :key="question.id"
                  :title="`问题 ${index + 1} - ${question.difficulty}`"
                >
                  <p class="question-text">{{ question.text }}</p>
                  <div class="question-tags">
                    <el-tag size="small" type="success">{{ getCategoryName(categoryId) }}</el-tag>
                    <el-tag size="small" type="info">{{ question.difficulty }}</el-tag>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Main Content Area Next Button -->
    <div class="main-next-button" v-if="currentStep === 1 && selectedCategories.length > 0">
      <el-button 
        type="primary" 
        @click="startGeneration"
        :loading="loading"
        size="large"
        class="floating-next"
        round
      >
        <span>生成面试题</span>
        <el-icon style="margin-left: 8px"><ArrowRight /></el-icon>
      </el-button>
    </div>

    <!-- Adjustment Popup Modal (moved from floating) -->
    <div v-if="showAdjustment" class="adjustment-popup" @click="toggleAdjustment">
      <div class="popup-content" @click.stop>
        <div class="popup-header">
          <h4>调整生成规则</h4>
          <button @click="toggleAdjustment">×</button>
        </div>
        
        <div class="suggestions">
          <span class="suggestion-label">快速调整：</span>
          <div class="suggestion-buttons">
            <el-button 
              v-for="example in promptExamples" 
              :key="example.text"
              size="small"
              @click="applySuggestion(example.text)"
            >
              {{ example.category }}
            </el-button>
          </div>
        </div>

        <el-input
          v-model="customPrompt"
          type="textarea"
          :rows="4"
          placeholder="例如：增加更多云计算和大数据的相关问题，难度中等偏上..."
          maxlength="200"
          show-word-limit
        />

        <div class="popup-actions">
          <el-button @click="clearCustomPrompt">清除</el-button>
          <el-button type="primary" @click="applyCustomAdjustment">
            应用调整
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ArrowLeft, ArrowRight, Setting, CircleClose, Edit, List, Loading, CircleCheck, Plus, Delete } from '@element-plus/icons-vue'

export default {
  name: 'QuestionGenerator',
  components: {
    ArrowLeft,
    ArrowRight,
    Setting,
    CircleClose,
    Edit,
    List,
    Loading,
    CircleCheck,
    Plus,
    Delete
  },
  data() {
    return {
      // Local state instead of Pinia store
      availableCategories: [
        { id: 'os', name: '操作系统', selected: false },
        { id: 'cpp', name: 'C/C++', selected: false },
        { id: 'network', name: '计算机网络', selected: false },
        { id: 'distributed', name: '分布式系统', selected: false },
        { id: 'database', name: '数据库', selected: false },
        { id: 'system_design', name: '系统设计', selected: false },
        { id: 'algorithm', name: '算法与数据结构', selected: false },
        { id: 'security', name: '系统安全', selected: false },
        { id: 'ml', name: '机器学习', selected: false },
        { id: 'frontend', name: '前端开发', selected: false },
        { id: 'backend', name: '后端开发', selected: false },
        { id: 'devops', name: 'DevOps', selected: false }
      ],
      selectedCategories: [],
      generatedQuestions: [],
      questionsByCategory: {},
      currentStep: 1,
      sidebarCollapsed: false,
      loading: false,
      showAdjustment: false,
      customPrompt: '',
      inlineCategoryName: '',
      promptExamples: [
        { category: '通用', text: '增加面试题的深度，稍微降低面试题的难度' },
        { category: 'C++', text: '题目范围扩充至C++20新版本' },
        { category: '操作系统', text: '增加更多Linux相关的问题' },
        { category: '网络', text: '加入更多实际生产环境的问题' },
        { category: '分布式', text: '与高并发场景结合，不要太空泛' }
      ]
    }
  },
  async created() {
    console.log('QuestionGenerator created')
  },
  mounted() {
    console.log('QuestionGenerator mounted, categories:', this.availableCategories.length)
  },
  methods: {
    getCategoryName(categoryId) {
      return this.availableCategories.find(c => c.id === categoryId)?.name || categoryId
    },
    
    toggleCategory(categoryId) {
      const index = this.selectedCategories.indexOf(categoryId)
      if (index > -1) {
        this.selectedCategories.splice(index, 1)
      } else {
        this.selectedCategories.push(categoryId)
      }
    },
    
    generateMoreCategories() {
      // Add more categories simulation
      this.$message.success('已添加更多技术领域')
      this.availableCategories = [...this.availableCategories]
    },
    
    startGeneration() {
      console.log('开始生成', this.selectedCategories)
      
      if (this.selectedCategories.length === 0) {
        this.$message.warning('请至少选择一个大类')
        return
      }
      
      this.loading = true
      
      // Simulate API call
      setTimeout(() => {
        this.loading = false
        this.generateQuestions()
        this.currentStep = 2
        this.sidebarCollapsed = true
        this.$message.success(`已为 ${this.selectedCategories.length} 个类别生成面试题`)
      }, 1000)
    },
    
    generateQuestions() {
      this.generatedQuestions = []
      this.questionsByCategory = {}
      
      this.selectedCategories.forEach(categoryId => {
        const categoryName = this.getCategoryName(categoryId)
        const questions = [
          {
            id: `q-${categoryId}-1`,
            text: `${categoryName}核心概念：请解释${categoryName}的基本原理和主要特点`,
            difficulty: '基础'
          },
          {
            id: `q-${categoryId}-2`,
            text: `${categoryName}实践挑战：在实际项目中遇到过哪些${categoryName}相关的难题？如何解决？`,
            difficulty: '中级'
          },
          {
            id: `q-${categoryId}-3`,
            text: `${categoryName}高级应用：如何优化${categoryName}在复杂场景下的性能？请提供具体方案`,
            difficulty: '高级'
          }
        ]
        
        this.questionsByCategory[categoryId] = questions
        this.generatedQuestions = [...this.generatedQuestions, ...questions]
      })
    },
    
    resetAll() {
      this.selectedCategories = []
      this.generatedQuestions = []
      this.questionsByCategory = {}
      this.currentStep = 1
      this.$message.success('已重置选择')
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    toggleAdjustment() {
      this.showAdjustment = !this.showAdjustment
    },
    
    applySuggestion(text) {
      this.customPrompt = text
    },
    
    applyCustomAdjustment() {
      this.generateQuestions()
      this.showAdjustment = false
      this.$message.success('已应用调整')
    },
    
    clearCustomPrompt() {
      this.customPrompt = ''
      this.showAdjustment = false
    },
    
    deleteCategory(categoryId) {
      // Don't allow deletion of built-in categories
      const protectedCategories = ['os', 'cpp', 'network', 'distributed', 'database', 'system_design', 'algorithm', 'security', 'ml', 'frontend', 'backend', 'devops']
      if (protectedCategories.includes(categoryId)) {
        this.$message.warning('系统内置领域不能删除')
        return
      }
      
      // Remove from selected if currently selected
      const selectedIndex = this.selectedCategories.indexOf(categoryId)
      if (selectedIndex > -1) {
        this.selectedCategories.splice(selectedIndex, 1)
      }
      
      // Remove from available categories
      this.availableCategories = this.availableCategories.filter(c => c.id !== categoryId)
      this.$message.success('技术领域已删除')
    },
    
    showDeleteButton(category) {
      // Only show delete button for custom categories
      const protectedCategories = ['os', 'cpp', 'network', 'distributed', 'database', 'system_design', 'algorithm', 'security', 'ml', 'frontend', 'backend', 'devops']
      return !protectedCategories.includes(category.id)
    },
    
    addInlineCategory() {
      if (!this.inlineCategoryName.trim()) return
      
      const name = this.inlineCategoryName.trim()
      const newId = name.toLowerCase().replace(/\s+/g, '_')
      
      // Check for duplicates
      const existing = this.availableCategories.find(c => c.id === newId)
      if (existing) {
        this.$message.warning('该技术领域已存在')
        return
      }
      
      this.availableCategories.push({
        id: newId,
        name: name,
        selected: false
      })
      
      this.inlineCategoryName = ''
      this.$message.success(`已添加技术领域：${name}`)
    },
    
    showAddCategoryDialog() {
      this.$prompt('请输入技术领域名称', '添加自定义领域', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\u4e00-\u9fa5\w\s-]+$/,
        inputErrorMessage: '请输入有效的技术领域名称'
      }).then(({ value }) => {
        const newId = value.toLowerCase().replace(/\s+/g, '_')
        this.availableCategories.push({
          id: newId,
          name: value,
          selected: false
        })
        this.$message.success(`已添加技术领域：${value}`)
      }).catch(() => {
        // cancelled
      })
    }
  }
}
</script>

<style scoped>
.question-generator-v2 {
  min-height: 100vh;
  display: flex;
  position: relative;
  background: #fafafa;
}

.sidebar-toggle {
  position: absolute;
  top: 20px;
  left: 280px;
  z-index: 10;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.sidebar-toggle.collapsed {
  left: 12px;
}

.sidebar {
  width: 280px;
  background: white;
  box-shadow: 2px 0 12px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.sidebar.collapsed {
  transform: translateX(-100%);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sidebar-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
.sidebar-actions .el-button {
  font-size: 14px;
  padding: 8px 12px;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
}

.selected-count {
  color: #7f8c8d;
  font-size: 14px;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}

.categories-list {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.category-slot {
  padding: 12px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-slot:hover {
  border-color: #409eff;
}

.category-slot.selected {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.generate-more {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: 2px solid #667eea;
}

.generate-more:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.category-content h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
}

.category-content p {
  margin: 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #e4e7ed;
}

.add-category-content {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
  width: 100%;
}

.add-category-text {
  margin: 0;
  font-weight: 500;
}

.add-manual {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.add-manual:hover {
  border-color: #409eff;
  background-color: #e6f2ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.inline-category-input {
  width: 100%;
  border: none;
  background: transparent;
}

.inline-category-input :deep(.el-input__wrapper) {
  box-shadow: none;
  background: transparent;
  padding: 0;
}

.inline-category-input :deep(.el-input__inner) {
  padding: 0 8px;
}

.category-name-center {
  text-align: center;
  font-weight: 600;
  margin-bottom: 6px;
}

.category-description-small {
  font-size: 12px;
  line-height: 1.3;
}

.category-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.delete-category-btn {
  color: #f56c6c;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  margin-left: 8px;
  opacity: 0.7;
  transition: all 0.2s;
}

.delete-category-btn:hover {
  opacity: 1;
  transform: scale(1.1);
  color: #ff4d4f;
}

.category-slot:hover .delete-category-btn {
  opacity: 1;
}

.main-content {
  flex: 1;
  transition: margin-left 0.3s ease;
  margin-left: 280px;
  padding: 20px;
}

.main-content.sidebar-collapsed {
  margin-left: 0;
}

.main-header {
  padding: 40px 20px;
  text-align: center;
}

.main-header h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.description {
  font-size: 16px;
  color: #7f8c8d;
  max-width: 600px;
  margin: 0 auto;
}

.step-container,
.questions-container {
  max-width: 1200px;
  margin: 0 auto;
}

.empty-guide {
  text-align: center;
  padding: 100px 20px;
}

.empty-guide h4 {
  margin: 20px 0 10px 0;
  color: #2c3e50;
}

.empty-guide p {
  color: #7f8c8d;
  margin-bottom: 20px;
}

.selection-summary {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 20px;
}

.loading {
  text-align: center;
  padding: 100px 20px;
}

.loading .el-icon {
  margin-bottom: 20px;
}

.generation-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.summary-text {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #67c23a;
  font-weight: 600;
}

.questions-grid {
  display: grid;
  gap: 30px;
}

.category-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.category-header h3 {
  margin: 0;
  color: #2c3e50;
}

.count {
  color: #7f8c8d;
  font-size: 14px;
}

.question-item {
  margin-bottom: 12px;
}

.question-text {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 8px;
}

.question-tags {
  display: flex;
  gap: 8px;
}

.main-next-button {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 1000;
}

.floating-next {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #409eff;
  color: white;
  padding: 16px 32px;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.3s;
  font-size: 14px;
}

.floating-next:hover {
  transform: translateY(-2px);
  background: #66b1ff;
  box-shadow: 0 6px 16px rgba(0,0,0,0.3);
}

.adjustment-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1001;
}

.popup-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(2px);
}

.popup-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  max-height: 80vh;
  overflow-y: auto;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.popup-header h4 {
  margin: 0;
  color: #2c3e50;
}

.popup-header button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.suggestions {
  margin-bottom: 20px;
}

.suggestion-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-right: 8px;
}

.suggestion-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.popup-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 100;
  }
  
  .main-content {
    margin-left: 0;
    padding: 10px;
  }
  
  .sidebar-toggle {
    left: 10px;
    top: 60px;
  }
  
  .adjustment-float-container {
    bottom: 20px;
    right: 20px;
  }
  
  .adjustment-trigger {
    padding: 12px 20px;
    font-size: 13px;
  }
  
  .popup-content {
    width: 95%;
    margin: 10px;
    max-height: 90vh;
  }
}
</style>