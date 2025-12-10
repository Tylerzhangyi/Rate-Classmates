<template>
  <aside class="sidebar">
    <div class="sidebar__header">
      <h2 class="sidebar__logo">Rate My Classmate</h2>
    </div>
    <nav class="sidebar__nav">
      <router-link to="/students" class="sidebar__item" active-class="sidebar__item--active">
        <i class="fas fa-users sidebar__icon"></i>
        <span>学生列表</span>
      </router-link>
      <router-link to="/leaderboard" class="sidebar__item" active-class="sidebar__item--active">
        <i class="fas fa-trophy sidebar__icon"></i>
        <span>排行榜</span>
      </router-link>
      <router-link to="/profile" class="sidebar__item" active-class="sidebar__item--active">
        <i class="fas fa-user sidebar__icon"></i>
        <span>个人中心</span>
      </router-link>
      <router-link 
        to="/apply-student" 
        class="sidebar__item" 
        active-class="sidebar__item--active"
      >
        <i class="fas fa-user-plus sidebar__icon"></i>
        <span>申请添加学生</span>
      </router-link>
      <router-link 
        v-if="!authStore.isAdmin"
        to="/apply-school" 
        class="sidebar__item" 
        active-class="sidebar__item--active"
      >
        <i class="fas fa-school sidebar__icon"></i>
        <span>申请添加学校</span>
      </router-link>
      <router-link 
        v-if="authStore.isAdmin"
        to="/apply-school" 
        class="sidebar__item" 
        active-class="sidebar__item--active"
      >
        <i class="fas fa-clipboard-check sidebar__icon"></i>
        <span>审核学校申请</span>
      </router-link>
    </nav>
    <div class="sidebar__footer">
      <button @click="handleLogout" class="sidebar__logout">
        <i class="fas fa-sign-out-alt sidebar__icon"></i>
        <span>退出登录</span>
      </button>
    </div>
  </aside>
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
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100vh;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 100;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar__header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.sidebar__logo {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.sidebar__nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.sidebar__item {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  color: #fff;
  text-decoration: none;
  transition: all 0.3s;
  font-weight: 500;
  border-left: 3px solid transparent;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.sidebar__item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.sidebar__item--active {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border-left-color: #fff;
}

.sidebar__icon {
  width: 20px;
  margin-right: 12px;
  font-size: 16px;
  text-align: center;
}

.sidebar__footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.sidebar__logout {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 12px 20px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 1);
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.sidebar__logout:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
}
</style>

