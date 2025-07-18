import { defineStore } from 'pinia'
import { interviewGenerationService } from '@/services/interviewGeneration.js'

/**
 * Interview Generation Store
 * Manages all state for interview question generation process
 */
export const useInterviewGenerationStore = defineStore('interview_generation', {
  state: () => ({
    // Step 1: Category Management
    categories: [],
    selectedCategories: [],
    displayedCategories: [],
    categoryCustomizations: {},
    
    // Step 2: Question Management  
    questions: {},
    questionAdjustments: {},
    currentCategory: null,
    
    // UI State
    currentStep: 1, // 1: categories, 2: questions
    loading: false,
    error: null,
    
    // Session Data
    session: {
      id: null,
      title: '',
      categories: [],
      questions: [],
      createdAt: null
    }
  }),

  getters: {
    hasGeneratedCategories: (state) => state.categories.length > 0,
    hasQuestionsForCategory: (state) => (categoryId) => {
      return state.questions[categoryId] && state.questions[categoryId].length > 0
    },
    totalQuestionsCount: (state) => {
      return Object.values(state.questions).reduce((total, questions) => total + questions.length, 0)
    },
    isCategorySelected: (state) => (categoryId) => {
      return state.selectedCategories.includes(categoryId)
    }
  },

  actions: {
    /**
     * Step 1: Generate initial categories
     */
    async generateInitialCategories() {
      this.loading = true
      this.error = null
      
      try {
        // For now, we'll use predefined categories since backend not ready
        const predefinedCategories = [
          { id: 'os', name: '操作系统', description: '操作系统原理与实践问题', selected: true },
          { id: 'cpp', name: 'C++', description: 'C++语言特性与高级特性', selected: true },
          { id: 'network', name: '网络', description: '网络协议与分布式系统', selected: true },
          { id: 'distributed', name: '分布式', description: '微服务架构与分布式理论', selected: true },
          { id: 'database', name: '数据库', description: 'SQL设计与优化', selected: true },
          { id: 'system_design', name: '系统设计', description: '高可用系统设计', selected: true }
        ]
        
        this.categories = predefinedCategories
        this.displayedCategories = [...predefinedCategories]
        this.selectedCategories = predefinedCategories.filter(c => c.selected).map(c => c.id)
        
        return predefinedCategories
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Toggle category selection
     */
    toggleCategory(categoryId) {
      const index = this.selectedCategories.indexOf(categoryId)
      if (index > -1) {
        this.selectedCategories.splice(index, 1)
      } else {
        this.selectedCategories.push(categoryId)
      }
    },

    /**
     * Generate more categories based on user input
     */
    async generateMoreCategories(customPrompt = '') {
      this.loading = true
      this.error = null
      
      try {
        // Mock additional categories
        const additionalCategories = [
          { id: 'algorithm', name: '算法与数据结构', description: '核心算法与复杂度分析', selected: false },
          { id: 'cloud', name: '云原生', description: 'Kubernetes与服务网格', selected: false },
          { id: 'security', name: '系统安全', description: '网络安全与权限控制', selected: false }
        ]
        
        this.displayedCategories = [...this.displayedCategories, ...additionalCategories]
        return additionalCategories
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Save category customizations
     */
    saveCategoryCustomization(categoryId, customization) {
      this.categoryCustomizations[categoryId] = customization
    },

    /**
     * Step 2: Generate questions for selected categories
     */
    async generateQuestions(options = {}) {
      this.loading = true
      this.error = null
      
      const params = {
        categories: this.selectedCategories,
        ...options
      }
      
      try {
        const response = await interviewGenerationService.generateQuestions(params)
        
        // Mock response structure
        const mockQuestions = {
          os: [
            {
              id: 'q1',
              text: '请解释操作系统中的进程和线程的区别，以及在Python中如何实现多进程和多线程？',
              difficulty: '中等',
              category: 'os'
            },
            {
              id: 'q2', 
              text: '什么是死锁？请描述死锁产生的四个必要条件，并给出预防死锁的方法。',
              difficulty: '困难',
              category: 'os'
            }
          ],
          cpp: [
            {
              id: 'q3',
              text: '请解释C++中的RAII原则，以及如何用智能指针避免内存泄漏。',
              difficulty: '中等',
              category: 'cpp'
            }
          ]
        }
        
        this.questions = mockQuestions
        this.session.categories = this.selectedCategories
        this.session.questions = mockQuestions
        
        return mockQuestions
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Regenerate questions for specific category
     */
    async regenerateQuestionsForCategory(categoryId, adjustments = '') {
      this.loading = true
      this.error = null
      
      try {
        const newQuestions = [
          {
            id: `q${Date.now()}`,
            text: `更新后的${this.categories.find(c => c.id === categoryId)?.name}问题：${adjustments}`,
            difficulty: '中等',
            category: categoryId,
            adjustment: adjustments
          }
        ]
        
        if (this.questions[categoryId]) {
          this.questions[categoryId] = [...this.questions[categoryId], ...newQuestions]
        } else {
          this.questions[categoryId] = newQuestions
        }
        
        return newQuestions
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Set current category for detail view
     */
    setCurrentCategory(categoryId) {
      this.currentCategory = categoryId
    },

    /**
     * Reset to step 1
     */
    resetGeneration() {
      this.categories = []
      this.selectedCategories = []
      this.displayedCategories = []
      this.categoryCustomizations = {}
      this.questions = {}
      this.questionAdjustments = {}
      this.currentCategory = null
      this.currentStep = 1
      this.error = null
    },

    /**
     * Save current session
     */
    async saveSession(title) {
      if (!title.trim()) {
        throw new Error('Session title is required')
      }

      const sessionData = {
        title: title.trim(),
        categories: this.selectedCategories,
        questions: this.questions,
        category_customizations: this.categoryCustomizations,
        created_at: new Date().toISOString()
      }

      try {
        const response = await interviewGenerationService.saveSession(sessionData)
        this.session = { ...sessionData, id: response.data.id }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    }
  }
})