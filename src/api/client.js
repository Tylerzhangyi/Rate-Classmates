import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
  withCredentials: false
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

