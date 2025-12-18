import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDataStore } from '../stores/data'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPassword.vue')
  },
  {
    path: '/schools',
    name: 'Schools',
    component: () => import('../views/Schools.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/school/:schoolId/students',
    name: 'SchoolStudents',
    component: () => import('../views/Students.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/student/:id',
    name: 'StudentDetail',
    component: () => import('../views/StudentDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/rate/:id',
    name: 'RateStudent',
    component: () => import('../views/RateStudent.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/Leaderboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/apply-school',
    name: 'ApplySchool',
    component: () => import('../views/ApplySchool.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/apply-student',
    name: 'ApplyStudent',
    component: () => import('../views/ApplyStudent.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const dataStore = useDataStore()
  
  // 如果目标路径是登录页，不恢复认证状态（避免登出后立即恢复）
  if (to.path !== '/login' && to.path !== '/register') {
    authStore.initAuth()
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    next('/schools')
  } else {
    if (to.meta.requiresAuth) {
      try {
        await dataStore.loadInitial()
      } catch (e) {
        // 忽略数据加载错误，页面自行展示提示
      }
    }
    next()
  }
})

export default router

