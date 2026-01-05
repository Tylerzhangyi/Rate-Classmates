import axios from 'axios'

const client = axios.create({
  // 服务器部署时，使用环境变量 VITE_API_BASE_URL 设置后端地址
  // 开发环境默认使用 localhost，生产环境应设置为服务器 IP 地址
  // 例如：VITE_API_BASE_URL=http://110.40.153.38:5001/api/
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://110.40.153.38:5001/api/',
  withCredentials: true  // 启用 cookie，用于 session 认证
})

client.interceptors.response.use(
  response => response,
  error => {
    const resp = error.response
    const message = resp?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default client

