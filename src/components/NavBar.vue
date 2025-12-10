<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/students">Rate My Classmate</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/students">学生列表</router-link>
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

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
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

