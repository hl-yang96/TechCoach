/**
 * Vue Router Configuration
 * File: frontend/src/router/index.js
 * Created: 2025-07-17
 * Purpose: Application routing configuration for TechCoach frontend
 */

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/interview',
    name: 'Interview',
    component: () => import('../views/Interview.vue'),
    children: [
      {
        path: '',
        name: 'InterviewSessions',
        component: () => import('../views/interview/Sessions.vue')
      },
      {
        path: 'session/:id',
        name: 'InterviewSession',
        component: () => import('../views/interview/Session.vue')
      },
      {
        path: 'generate',
        name: 'GenerateQuestions',
        component: () => import('../views/interview/Generate.vue')
      }
    ]
  },
  {
    path: '/upload',
    name: 'Documents',
    component: () => import('../views/Documents.vue')
  },
  {
    path: '/career',
    name: 'Career',
    component: () => import('../views/Career.vue'),
    children: [
      {
        path: '',
        name: 'ResumeAnalysis',
        component: () => import('../views/career/ResumeAnalysis.vue')
      },
      {
        path: 'optimization',
        name: 'ResumeOptimization',
        component: () => import('../views/career/ResumeOptimization.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router