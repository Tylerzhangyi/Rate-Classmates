import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 8805,
    strictPort: true, // 如果端口被占用，报错而不是自动切换
    // 允许通过域名或 IP 访问 Vite Dev Server
    allowedHosts: ['tyler.yunguhs.com', '110.40.153.38'],
    watch: {
      ignored: ['**/.venv/**', '**/node_modules/**', '**/.git/**']
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

