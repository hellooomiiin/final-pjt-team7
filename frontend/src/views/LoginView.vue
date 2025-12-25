<template>
  <div class="reviews-container">
    <div class="reviews-wrapper">
      <div class="edit-card">
        <button @click="goHome" class="close-button">×</button>
        <h2 class="edit-title">로그인</h2>
        <p class="edit-subtitle">Mood-Match에 오신 것을 환영합니다</p>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email" class="form-label">이메일</label>
            <div class="input-wrapper">
              <span class="input-icon">✉️</span>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                placeholder="example@email.com"
                required
              />
            </div>
          </div>
          <div class="form-group">
            <label for="password" class="form-label">비밀번호</label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                placeholder="********"
                required
              />
            </div>
          </div>
          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" />
              <span>로그인 상태 유지</span>
            </label>
            <a href="#" class="forgot-password">비밀번호 찾기</a>
          </div>
          <div v-if="showLogoutMessage" class="alert alert-warning">
            세션이 만료되어 자동으로 로그아웃되었습니다. 다시 로그인해주세요.
          </div>
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          <button type="submit" class="btn-submit">
            로그인
          </button>
          <div class="text-center register-link">
            <span>계정이 없으신가요? </span>
            <router-link to="/register">회원가입</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const rememberMe = ref(false)
    const showLogoutMessage = ref(false)

    // URL 쿼리 파라미터 확인
    onMounted(() => {
      if (route.query.logout === 'expired') {
        showLogoutMessage.value = true
        // 쿼리 파라미터 제거
        router.replace({ query: {} })
      }
    })

    const handleLogin = async () => {
      error.value = ''
      showLogoutMessage.value = false
      const result = await authStore.login(email.value, password.value)
      
      if (result.success) {
        router.push('/')
      } else {
        error.value = result.error
      }
    }

    const goHome = () => {
      router.push('/')
    }

    return {
      email,
      password,
      error,
      rememberMe,
      showLogoutMessage,
      handleLogin,
      goHome
    }
  }
}
</script>

<style scoped>
.reviews-container {
  min-height: calc(100vh - 80px);
  background-color: #000000;
  color: #ffffff;
  padding: 2rem 0;
}

.reviews-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  position: relative;
}

.edit-card {
  background-color: #1a1a1a;
  padding: 22px;
  border-radius: 8px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #333333;
  border: none;
  color: #ffffff;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background-color 0.2s;
  z-index: 10;
}

.close-button:hover {
  background-color: #444444;
}

.close-button:focus {
  outline: none;
}

.edit-title {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.edit-subtitle {
  color: #999999;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  color: #ffffff;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  z-index: 1;
}

.input-wrapper .form-control {
  width: 100%;
  padding-left: 45px;
  background-color: #333333;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  height: 50px;
  border-radius: 4px;
  font-size: 1rem;
}

.input-wrapper .form-control:focus {
  background-color: #333333;
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1);
}

.input-wrapper .form-control::placeholder {
  color: #666666;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  color: #ffffff;
  cursor: pointer;
  font-size: 0.9rem;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.forgot-password {
  color: #999999;
  text-decoration: underline;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: #ffffff;
}

.alert {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.alert-danger {
  background-color: #1a1a1a;
  border: 1px solid rgba(220, 53, 69, 0.5);
  color: #dc3545;
}

.alert-warning {
  background-color: #1a1a1a;
  border: 1px solid rgba(255, 193, 7, 0.5);
  color: #ffc107;
}

.btn-submit {
  width: 100%;
  border: none;
  background-color: #1a1a1a;
  color: #ffffff;
  height: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-bottom: 1rem;
}

.btn-submit:hover {
  background-color: #252525;
}

.register-link {
  color: #999999;
  font-size: 0.9rem;
}

.register-link a {
  color: #ffffff;
  font-weight: bold;
  text-decoration: underline;
  transition: color 0.2s;
}

.register-link a:hover {
  color: #cccccc;
}

@media (max-width: 768px) {
  .reviews-wrapper {
    padding: 0 0.5rem;
  }

  .edit-card {
    padding: 1.5rem;
  }
}
</style>
