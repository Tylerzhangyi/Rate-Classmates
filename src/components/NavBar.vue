<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/schools" class="brand-link">
          <img src="/images/favicon.png" alt="Logo" class="brand-icon" />
          <span>Rate My Classmate</span>
        </router-link>
      </div>
      <div class="nav-links">
        <router-link to="/schools">评分大厅</router-link>
        <router-link to="/leaderboard">排行榜</router-link>
        <router-link to="/apply-student">申请学生</router-link>
        <router-link to="/apply-school">申请学校</router-link>
        <router-link to="/profile">个人中心</router-link>
        <button @click="handleLogout" class="btn-logout">退出</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import client from '../api/client'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  // 先清除状态，确保路由守卫检测到未登录
  authStore.currentUser = null
  localStorage.removeItem('currentUser')
  
  try {
    await client.post('auth/logout')
  } catch (e) {
    // 即使后端登出失败，前端状态已清除
    console.error('登出失败:', e)
  }
  
  // 使用 replace 替换当前历史记录，确保跳转到登录页
  router.replace('/login').catch(() => {
    // 如果路由跳转失败，使用 window.location 强制跳转
    window.location.href = '/login'
  })
}
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 20px;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand a {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
  transition: color 0.3s;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: drop-shadow(0 1px 2px rgba(255, 255, 255, 0.5));
  transition: transform 0.3s;
  display: block;
  flex-shrink: 0;
}

.brand-link:hover .brand-icon {
  transform: scale(1.1);
}

.nav-brand a:hover {
  color: #fff;
  text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #fff;
  text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
}

.btn-logout {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: 1px solid #dc3545;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-logout:hover {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.4);
}
</style>

