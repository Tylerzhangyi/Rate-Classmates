import axios from 'axios'

const client = axios.create({
  // 注意：localhost 与 127.0.0.1 在浏览器 SameSite 规则下被视为不同站点，
  // 会导致 Django session cookie 不随请求发送，从而出现“已登录但接口 401 未登录”。
  // 因此前后端都统一用 localhost。
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api/',
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

