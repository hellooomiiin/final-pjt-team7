import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 모킹 모드 (백엔드 통신 없이 사용)
const MOCK_MODE = false

// 모킹 지연 함수
const delay = (ms = 500) => new Promise(resolve => setTimeout(resolve, ms))

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    if (MOCK_MODE) {
      await delay(500)
      // 간단한 모킹: 아무 아이디/비밀번호로 로그인 가능
      if (email && password) {
        const mockUser = {
          id: 1,
          email: email,
          nickname: email.split('@')[0],
          created_at: '2024-01-01T00:00:00Z'
        }
        token.value = 'mock_access_token_' + Date.now()
        refreshToken.value = 'mock_refresh_token_' + Date.now()
        user.value = mockUser
        
        localStorage.setItem('access_token', token.value)
        localStorage.setItem('refresh_token', refreshToken.value)
        
        return { success: true }
      } else {
        return { 
          success: false, 
          error: '이메일과 비밀번호를 입력해주세요.' 
        }
      }
    }
    
    // 실제 API 호출
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
    if (MOCK_MODE) {
      await delay(500)
      // 간단한 모킹: 회원가입 항상 성공
      const mockUser = {
        id: Date.now(),
        email: userData.email,
        nickname: userData.nickname,
        created_at: new Date().toISOString()
      }
      token.value = 'mock_access_token_' + Date.now()
      refreshToken.value = 'mock_refresh_token_' + Date.now()
      user.value = mockUser
      
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      
      return { success: true }
    }
    
      // 실제 API 호출
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
    if (MOCK_MODE) {
      await delay(300)
      if (token.value) {
        user.value = {
          id: 1,
          email: 'test@test.com',
          nickname: 'testuser',
          created_at: '2024-01-01T00:00:00Z'
        }
        return { success: true }
      }
      return { success: false, error: '로그인이 필요합니다.' }
    }
    
    // 실제 API 호출 (현재 사용 안 함)
    try {
      const api = (await import('@/api')).default
      const response = await api.get('/accounts/profile/')
      user.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
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
    fetchProfile
  }
})

