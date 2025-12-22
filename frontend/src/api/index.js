import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // 로그인/회원가입 API는 Interceptor에서 제외
    const isAuthEndpoint = originalRequest.url?.includes('/accounts/login/') || 
                          originalRequest.url?.includes('/accounts/register/')

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      originalRequest._retry = true
      const authStore = useAuthStore()

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/accounts/token/refresh/`,
          { refresh: authStore.refreshToken }
        )

        authStore.token = response.data.access
        localStorage.setItem('access_token', response.data.access)

        originalRequest.headers.Authorization = `Bearer ${response.data.access}`
        return api(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        // 로그인 페이지가 아닐 때만 리다이렉트
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api

