import api from './api.js'

/**
 * Interview Question Generation Service
 * Handles category management and question generation
 */

export const interviewGenerationService = {
  /**
   * Get available categories for interview questions
   */
  getCategories() {
    return api.get('/categories')
  },

  /**
   * Generate more categories based on existing selections
   */
  generateMoreCategories(selectedCategories, customPrompt = '') {
    return api.post('/categories/generate-more', {
      selected_categories: selectedCategories,
      custom_prompt: customPrompt
    })
  },

  /**
   * Generate questions for selected categories with customizable parameters
   */
  generateQuestions(params) {
    return api.post('/questions/generate', {
      categories: params.categories,
      difficulty: params.difficulty || 'medium',
      category_adjustments: params.categoryAdjustments || {},
      step_by_step: params.stepByStep || false,
      custom_instructions: params.customInstructions || '',
      generate_mode: params.generateMode || 'single'
    })
  },

  /**
   * Regenerate questions for a specific category with adjustments
   */
  regenerateQuestions(categoryId, adjustments = {}) {
    return api.post(`/categories/${categoryId}/regenerate`, {
      adjustments
    })
  },

  /**
   * Save generated interview session
   */
  saveSession(sessionData) {
    return api.post('/interview/sessions', sessionData)
  },

  /**
   * Get user's saved interview sessions
   */
  getSessions() {
    return api.get('/interview/sessions')
  },

  /**
   * Get specific session details
   */
  getSession(sessionId) {
    return api.get(`/interview/sessions/${sessionId}`)
  },

  /**
   * Update session data
   */
  updateSession(sessionId, updates) {
    return api.put(`/interview/sessions/${sessionId}`, updates)
  }
}

export default interviewGenerationService