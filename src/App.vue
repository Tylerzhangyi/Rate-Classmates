<template>
  <div id="app">
    <Sidebar v-if="isAuthenticated" />
    <div class="main-content" :class="{ 'main-content--with-sidebar': isAuthenticated }">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
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
</style>

