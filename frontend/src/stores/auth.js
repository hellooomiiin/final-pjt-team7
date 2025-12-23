import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    try {
      const api = (await import('@/api')).default
      const response = await api.post('/accounts/login/', { email, password })
      token.value = response.data.tokens.access
      refreshToken.value = response.data.tokens.refresh
      user.value = response.data.user
      
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || '로그인에 실패했습니다.' 
      }
    }
  }

  const register = async (userData) => {
    try {
      const api = (await import('@/api')).default
      
      const registerData = {
        username: userData.username,
        email: userData.email,
        nickname: userData.nickname,
        password: userData.password,
        password_confirm: userData.password_confirm
      }
    
      const response = await api.post('/accounts/register/', registerData)
      
      if (response.data && response.data.tokens) {
        token.value = response.data.tokens.access
        refreshToken.value = response.data.tokens.refresh
        user.value = response.data.user
        
        localStorage.setItem('access_token', token.value)
        localStorage.setItem('refresh_token', refreshToken.value)
        
        return { success: true }
      } else {
        return { 
          success: false, 
          error: '회원가입 응답 형식이 올바르지 않습니다.' 
        }
      }
    } catch (error) {
      console.error('회원가입 에러:', error)
      
      // 에러 메시지 처리
      let errorMessage = '회원가입에 실패했습니다.'
      
      if (error.response?.data) {
        const errorData = error.response.data
        
        // DRF ValidationError 형식 처리
        if (typeof errorData === 'object') {
          const errorMessages = []
          for (const key in errorData) {
            if (Array.isArray(errorData[key])) {
              errorMessages.push(...errorData[key])
            } else if (typeof errorData[key] === 'string') {
              errorMessages.push(errorData[key])
            } else {
              errorMessages.push(`${key}: ${JSON.stringify(errorData[key])}`)
            }
          }
          errorMessage = errorMessages.length > 0 
            ? errorMessages.join(', ')
            : errorMessage
        } else if (typeof errorData === 'string') {
          errorMessage = errorData
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      return { 
        success: false, 
        error: errorMessage
      }
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const fetchProfile = async () => {
    try {
      const api = (await import('@/api')).default
      const response = await api.get('/accounts/profile/')
      user.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  // 토큰 유효성 검증
  const checkAuth = async () => {
    if (token.value) {
      // 토큰이 있으면 프로필 조회로 유효성 확인
      const result = await fetchProfile()
      if (!result.success) {
        // 토큰이 유효하지 않으면 로그아웃
        logout()
      }
    }
  }

  return {
    user,
    token,
    refreshToken,
    isAuthenticated,
    login,
    register,
    logout,
    fetchProfile,
    checkAuth
  }
})

