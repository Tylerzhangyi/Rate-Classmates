import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref(null)
  const users = ref([
    // 模拟用户数据
    {
      id: '1',
      account: 'test',
      password: 'test',
      name: '张三',
      role: 'user'
    },
    {
      id: '2',
      account: 'student002',
      password: '123456',
      name: '李四',
      role: 'user'
    },
    {
      id: 'admin',
      account: 'admin',
      password: 'admin123',
      name: '管理员',
      role: 'admin'
    }
  ])

  const isAuthenticated = computed(() => currentUser.value !== null)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')

  function login(account, password) {
    const user = users.value.find(
      u => (u.account === account || u.account.includes(account)) && u.password === password
    )
    if (user) {
      currentUser.value = { ...user }
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
      return { success: true, message: '登录成功' }
    }
    return { success: false, message: '账号或密码错误' }
  }

  function register(userData) {
    const newUser = {
      id: String(users.value.length + 1),
      ...userData,
      role: 'user', // 默认角色为普通用户
      created_at: new Date().toISOString()
    }
    users.value.push(newUser)
    currentUser.value = { ...newUser }
    localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    return { success: true, message: '注册成功' }
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem('currentUser')
  }

  function initAuth() {
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      currentUser.value = JSON.parse(savedUser)
    }
  }

  return {
    currentUser,
    users,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    initAuth
  }
})

