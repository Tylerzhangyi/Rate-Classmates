<template>
  <div id="app">
    <Sidebar v-if="isAuthenticated" />
    <div class="main-content" :class="{ 'main-content--with-sidebar': isAuthenticated }">
      <router-view v-slot="{ Component, route }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  authStore.initAuth()
})
</script>

<style>
#app {
  min-height: 100vh;
}

.main-content {
  min-height: 100vh;
}

.main-content--with-sidebar {
  margin-left: 250px;
  padding: 20px;
}

/* 页面切换动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>

