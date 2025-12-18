import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref(null)
  const isAuthenticated = computed(() => currentUser.value !== null)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')
  const loading = ref(false)
  const error = ref('')

  async function login(account, password) {
    loading.value = true
    error.value = ''
    try {
      const res = await client.post('auth/login', { account, password })
      const user = res.data.data
      currentUser.value = { ...user, name: user.account, id: user.user_id }
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
      return { success: true, message: res.data.message }
    } catch (e) {
      error.value = e.message
      return { success: false, message: e.message }
    } finally {
      loading.value = false
    }
  }

  async function register(account, password) {
    loading.value = true
    error.value = ''
    try {
      const res = await client.post('auth/register', { account, password })
      const user = res.data.data
      currentUser.value = { ...user, name: user.account, id: user.user_id }
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
      return { success: true, message: res.data.message }
    } catch (e) {
      error.value = e.message
      return { success: false, message: e.message }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    error.value = ''
    try {
      await client.post('auth/logout')
      currentUser.value = null
      localStorage.removeItem('currentUser')
      return { success: true, message: '登出成功' }
    } catch (e) {
      // 即使后端登出失败，也清除前端状态
      currentUser.value = null
      localStorage.removeItem('currentUser')
      error.value = e.message
      return { success: false, message: e.message }
    } finally {
      loading.value = false
    }
  }

  function initAuth() {
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      currentUser.value = JSON.parse(savedUser)
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    loading,
    error,
    login,
    register,
    logout,
    initAuth
  }
})

