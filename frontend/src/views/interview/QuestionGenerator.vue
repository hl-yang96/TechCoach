<template>
  <div class="question-generator-v2">

    <!-- Collapsible Sidebar -->
    <aside 
      class="sidebar" 
          >
      <div class="sidebar-header">
        <h3>技术领域</h3>
      </div>

      <div class="sidebar-content">
        <div class="categories-list">
          <div
            v-for="category in availableCategories" 
            :key="category.id"
            class="category-slot"
            :class="{
              disabled: loading,
              selected: currentCategory && currentCategory.id === category.id
            }"
            @click="selectCategory(category.id)"
          >
            <div class="category-content">
              <h4>{{ category.name }}</h4>
            </div>
            <el-button
              type="danger"
              size="small"
              circle
              plain
              @click.stop="deleteCategory(category.name)"
              style="border-radius: 50%; padding: 8px; color: #ff4949;"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>

          <!-- Manual Add Input -->
          <div class="manual-add category-slot">
            <div class="category-content">
              <el-input
                v-model="newTechDomain"
                placeholder="输入技术领域"
                size="small"
                class="manual-input"
                @keyup.enter="addTechDomain"
                :disabled="loading"
                clearable
                maxlength="20"
                show-word-limit
              />
            </div>
            <el-button
              type="primary"
              size="small"
              circle
              plain
              @click="addTechDomain"
              :loading="loading"
              :disabled="!newTechDomain.trim()"
              style="border-radius: 50%; padding: 8px;"
            >
              <el-icon><Plus /></el-icon>
            </el-button>
          </div>

          <!-- Generate More Button -->
          <div
            class="generate-more category-slot"
            :class="{ disabled: loading }"
            @click="generateMoreCategories"
          >
            <div class="category-content">
              <h4>🚀 智能扩展</h4>
              <p>基于AI生成适合的技术领域</p>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-area">
        <!-- 未选择技术领域时的状态 -->
        <div v-if="!currentCategory" class="empty-state">
          <div class="empty-content">
            <h3>欢迎使用面试题生成器</h3>
            <p>请从左侧选择一个技术领域开始生成面试题</p>
          </div>
        </div>

        <!-- 已选择技术领域时的状态 -->
        <div v-else class="questions-section">
          <div class="section-header">
            <h2>{{ currentCategory.name }} - 题库</h2>
          </div>

          <!-- 加载状态 -->
          <div v-if="questionsLoading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <p>正在加载题库...</p>
          </div>

          <!-- 无题目时显示生成按钮 -->
          <div v-else-if="currentQuestions.length === 0" class="empty-questions">
            <div class="empty-content">
              <h3>{{ currentCategory.name }}</h3>
              <p>该技术领域暂无题库，点击下方按钮开始生成面试题</p>
              <el-button
                type="primary"
                size="large"
                @click="generateQuestions"
                :loading="generating"
                :icon="Plus"
                class="generate-btn"
              >
                {{ generating ? '正在生成题库...' : '生成题库' }}
              </el-button>
            </div>
          </div>

          <!-- 显示题目列表 -->
          <div v-else class="questions-list">
            <div class="questions-header">
              <span>共 {{ currentQuestions.length }} 道题目</span>
              <el-button
                type="primary"
                size="small"
                @click="generateQuestions"
                :loading="generating"
              >
                {{ generating ? '正在生成...' : '重新生成' }}
              </el-button>
            </div>

            <div class="questions-content">
              <div
                v-for="(question, index) in currentQuestions"
                :key="question.id || index"
                class="question-item"
              >
                <div class="question-number">{{ index + 1 }}</div>
                <div class="question-text">{{ question.question_text }}</div>
                <el-button
                  type="danger"
                  size="small"
                  circle
                  plain
                  @click.stop="deleteQuestion(question.id)"
                  class="delete-question-btn"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>

            <!-- 手动添加问题 -->
            <div class="add-question-section">
              <div class="add-question-item">
                <div class="question-number-placeholder"></div>
                <el-input
                  v-model="newQuestionText"
                  placeholder="输入新的面试题..."
                  size="default"
                  class="add-question-input"
                  @keyup.enter="addQuestion"
                  :disabled="addingQuestion"
                />
                <el-button
                  type="primary"
                  size="small"
                  circle
                  plain
                  @click="addQuestion"
                  :loading="addingQuestion"
                  :disabled="!newQuestionText.trim()"
                  class="add-question-btn"
                >
                  <el-icon><Plus /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import {
  Setting,
  Delete,
  Plus,
  Loading
} from '@element-plus/icons-vue'

export default {
  name: 'QuestionGenerator',
  components: {
    Setting,
    Delete,
    Plus,
    Loading
  },
  data() {
    return {
      availableCategories: [],
      loading: false,
      currentCategory: null,
      newTechDomain: '',
      currentQuestions: [],
      questionsLoading: false,
      generating: false,
      newQuestionText: '',
      addingQuestion: false
    }
  },
    
  async mounted() {
    console.log('QuestionGenerator mounted')
    await this.loadSavedTechDomains()
  },
    
  methods: {
    async loadSavedTechDomains() {
      this.loading = true
      try {
        const response = await this.$axios.get('/api/questions/tech-domains')
        this.availableCategories = response.data.domains.map(domain => ({
          id: domain.name, // 使用 name 作为 id，因为 name 是主键
          name: domain.name,
        }))
      } catch (error) {
        console.error('Failed to load tech domains:', error)
        this.$message.error('加载技术领域失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    async generateMoreCategories() {
      this.loading = true
      try {
        const response = await this.$axios.post('/api/questions/tech-domains/generate', {})

        const newDomains = response.data.domains

        if (!Array.isArray(newDomains) || newDomains.length === 0) {
          this.$message.info('暂时没有更多新的技术领域推荐')
        } else {
          const existingNames = this.availableCategories.map(c => c.name)
          const newCategories = newDomains.filter(domain =>
            !existingNames.includes(domain.name)
          ).map(domain => ({
            id: domain.name, // 使用 name 作为 id，因为 name 是主键
            name: domain.name,
          }))

          this.availableCategories = [...this.availableCategories, ...newCategories]
          this.$message.success(`已添加 ${newCategories.length} 个新的技术领域`)
        }

      } catch (error) {
        console.error('Failed to generate domains:', error)
        this.$message.error('获取技术领域失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    
    async selectCategory(categoryId) {
      const category = this.availableCategories.find(c => c.id === categoryId)
      if (!category) return

      this.currentCategory = category
      this.newQuestionText = '' // 清空输入框
      this.$message.success(`已选择技术领域：${category.name}`)

      // 查询当前领域的所有问题
      await this.fetchQuestions(categoryId)
    },

    async fetchQuestions(categoryId) {
      this.questionsLoading = true
      this.currentQuestions = []

      try {
        const response = await this.$axios.post('/api/questions/tech-domains/questions/get_all', {
          domain_name: categoryId
        })
        this.currentQuestions = response.data.questions || []
      } catch (error) {
        console.error('Failed to fetch questions:', error)
        this.$message.error('获取题库失败，请稍后重试')
        this.currentQuestions = []
      } finally {
        this.questionsLoading = false
      }
    },

    async generateQuestions() {
      if (!this.currentCategory) return

      this.generating = true
      try {
        const response = await this.$axios.post('/api/questions/tech-domains/questions/generate', {
          domain_name: this.currentCategory.id
        })
        this.currentQuestions = response.data.questions || []
        if (this.currentQuestions.length === 0) {
          this.$message.info('暂时无法生成题库')
        } else {
          this.$message.success(`已生成 ${this.currentQuestions.length} 道题目`)
        }
      } catch (error) {
        console.error('Failed to generate questions:', error)
        this.$message.error('生成题库失败，请稍后重试')
      } finally {
        this.generating = false
      }
    },

    async deleteQuestion(questionId) {
      if (!questionId) {
        this.$message.error('无效的问题ID')
        return
      }

      try {
        await this.$axios.post('/api/questions/tech-domains/questions/delete', {
          question_id: questionId
        })

        // 从当前问题列表中移除
        this.currentQuestions = this.currentQuestions.filter(q => q.id !== questionId)
        this.$message.success('问题删除成功')
      } catch (error) {
        console.error('Failed to delete question:', error)
        this.$message.error('删除问题失败，请稍后重试')
      }
    },

    async addQuestion() {
      if (!this.newQuestionText.trim() || !this.currentCategory) {
        return
      }

      this.addingQuestion = true
      try {
        const response = await this.$axios.post('/api/questions/tech-domains/questions/manual', {
          domain_name: this.currentCategory.id,
          question_text: this.newQuestionText.trim()
        })

        // 添加到当前问题列表
        const newQuestion = {
          id: response.data.id,
          domain_name: response.data.domain_name,
          question_text: response.data.question_text,
          user_answer: null,
          generated_answer: null,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }

        this.currentQuestions.push(newQuestion)
        this.newQuestionText = ''
        this.$message.success('问题添加成功')
      } catch (error) {
        console.error('Failed to add question:', error)
        this.$message.error('添加问题失败，请稍后重试')
      } finally {
        this.addingQuestion = false
      }
    },
    
    async deleteCategory(categoryId) {
      const category = this.availableCategories.find(c => c.id === categoryId)
      if (!category) {
        this.$message.info('系统领域不可删除')
        return
      }

      try {
        // 使用 POST 请求删除，避免 URL 路径中特殊字符（如 "/"）的问题
        await this.$axios.post('/api/questions/tech-domains/delete', {
          name: categoryId
        })
        this.availableCategories = this.availableCategories.filter(c => c.id !== categoryId)

        // 如果删除的是当前正在查看的类别，清空当前类别和问题
        if (this.currentCategory && this.currentCategory.id === categoryId) {
          this.currentCategory = null
          this.currentQuestions = []
          this.newQuestionText = '' // 清空输入框
        }

        this.$message.success(`已删除技术领域：${category.name}`)
      } catch (error) {
        console.error('Delete failed:', error)
        this.$message.error('删除失败，请稍后重试')
      }
    },
    
    async addTechDomain() {
      if (!this.newTechDomain.trim()) return

      this.loading = true
      try {
        const response = await this.$axios.post('/api/questions/tech-domains/manual', {
          name: this.newTechDomain.trim()
        })

        const existingNames = this.availableCategories.map(c => c.name)
        if (!existingNames.includes(response.data.name)) {
          this.availableCategories.push({
            id: response.data.name, // 使用 name 作为 id，因为 name 是主键
            name: response.data.name,
          })
          this.$message.success(`已成功添加技术领域：${response.data.name}`)
        } else {
          this.$message.info('该技术领域已存在')
        }

        this.newTechDomain = ''
      } catch (error) {
        console.error('Failed to add tech domain:', error)
        if (error.response && error.response.status === 409) {
          this.$message.warning('该技术领域已存在')
        } else {
          this.$message.error('添加技术领域失败，请稍后重试')
        }
      } finally {
        this.loading = false
      }
    },
    
    
    getCategoryName(categoryName) {
      const category = this.availableCategories.find(c => c.name === categoryName)
      return category ? category.name : categoryName
    }
  }
}
</script>

<style scoped>
.question-generator-v2 {
  min-height: 100vh;
  display: flex;
  background: #f5f5f5;
  position: relative;
}

.sidebar {
  width: 280px;
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sidebar-header h3 {
  margin: 0;
  color: #2c3e50;
}

.admin-count {
  color: #666;
  font-size: 14px;
}

.sidebar-content {
  padding: 16px;
}

.manual-add-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #f8f9fa;
}

.manual-add-section:hover {
  border-color: #409eff;
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-slot {
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.category-slot:hover {
  border-color: #409eff;
}

.category-slot .el-button {
  flex-shrink: 0;
  margin-left: 8px;
  margin-top: -4px;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.category-slot:hover .el-button {
  opacity: 1;
}

.category-slot.selected {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.category-slot.selected h4 {
  color: white;
}

.category-slot.selected:hover {
  background-color: #337ecc;
  border-color: #337ecc;
}

.category-content h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  padding-right: 24px;
  line-height: 1.4;
}

.generate-more {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.generate-more:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 40px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.empty-content {
  text-align: center;
  color: #606266;
}

.empty-content h3 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 500;
}

.empty-content p {
  margin: 0 0 24px 0;
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
}

.generate-btn {
  padding: 12px 32px !important;
  font-size: 16px !important;
  border-radius: 8px !important;
}

.selected-categories h3 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}





/* 手动添加技术领域的样式 */
.manual-add {
  background-color: #f8f9fa;
  border: 2px dashed #d1d5db;
  color: #6b7280;
}

.manual-add:hover {
  border-color: #9ca3af;
  background-color: #f3f4f6;
}

.manual-add .category-content {
  flex: 1;
  padding-right: 8px;
}

.manual-add .manual-input {
  width: 100%;
}

.manual-add .manual-input .el-input__inner {
  border: none;
  background: transparent;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
}

.manual-add .manual-input .el-input__inner::placeholder {
  color: #9ca3af;
  font-style: italic;
}

.manual-add .manual-input .el-input__inner:focus {
  background: transparent;
  border: none;
  box-shadow: none;
}

/* 手动添加按钮样式 */
.manual-add .el-button {
  min-width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.manual-add .el-button:not(.is-disabled) {
  color: #409eff;
  border-color: #409eff;
}

.manual-add .el-button:not(.is-disabled):hover {
  background-color: #409eff;
  color: white;
  transform: scale(1.05);
}

.manual-add .el-button.is-disabled {
  color: #c0c4cc;
  border-color: #e4e7ed;
  cursor: not-allowed;
}

/* 删除按钮样式优化 */
.category-slot .el-button--danger {
  min-width: 32px;
  height: 32px;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.category-slot .el-button--danger:hover {
  opacity: 1;
  background-color: #f56c6c;
  border-color: #f56c6c;
  color: white;
  transform: scale(1.05);
}

.category-slot .el-button--danger .el-icon {
  font-size: 14px;
}

/* 问题相关样式 */
.questions-section {
  padding: 20px;
}

.section-header h2 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 24px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #606266;
}

.loading-state .el-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.empty-questions {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.questions-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background: #f8f9fa;
  border-radius: 8px 8px 0 0;
}

.questions-header span {
  color: #606266;
  font-weight: 500;
}

.questions-content {
  padding: 0;
}

.question-item {
  display: flex;
  align-items: flex-start;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
  position: relative;
}

.question-item:last-child {
  border-bottom: none;
}

.question-item:hover {
  background-color: #f8f9fa;
}

.question-item:hover .delete-question-btn {
  opacity: 1;
}

.question-number {
  background: #409eff;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 16px;
  flex-shrink: 0;
}

.question-text {
  color: #303133;
  line-height: 1.6;
  font-size: 14px;
  flex: 1;
}

/* 删除问题按钮 */
.delete-question-btn {
  margin-left: 12px;
  opacity: 0;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.delete-question-btn:hover {
  background-color: #f56c6c;
  border-color: #f56c6c;
  color: white;
  transform: scale(1.05);
}

/* 添加问题区域 */
.add-question-section {
  border-top: 1px solid #ebeef5;
  background-color: #fafafa;
}

.add-question-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 16px;
}

.question-number-placeholder {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  /* 透明占位符，保持与上面题目的对齐 */
}

.add-question-input {
  flex: 1;
}

.add-question-input .el-input__inner {
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 14px;
}

.add-question-input .el-input__inner:focus {
  border-color: #409eff;
}

.add-question-btn {
  flex-shrink: 0;
}

.add-question-btn:not(.is-disabled) {
  color: #67c23a;
  border-color: #67c23a;
}

.add-question-btn:not(.is-disabled):hover {
  background-color: #67c23a;
  color: white;
  transform: scale(1.05);
}

.add-question-btn.is-disabled {
  color: #c0c4cc;
  border-color: #e4e7ed;
  cursor: not-allowed;
}
</style>