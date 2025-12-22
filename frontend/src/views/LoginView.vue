<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="login-card">
            <h2 class="login-title">로그인</h2>
            <p class="login-subtitle">Mood-Match에 오신 것을 환영합니다</p>
            <form @submit.prevent="handleLogin">
              <div class="form-group mb-3">
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
              <div class="form-group mb-3">
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
              <div class="d-flex justify-content-between align-items-center mb-4">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="rememberMe" />
                  <span>로그인 상태 유지</span>
                </label>
                <a href="#" class="forgot-password">비밀번호 찾기</a>
              </div>
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              <button type="submit" class="btn btn-login w-100 mb-3">
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
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const rememberMe = ref(false)

    const handleLogin = async () => {
      error.value = ''
      const result = await authStore.login(email.value, password.value)
      
      if (result.success) {
        router.push('/')
      } else {
        error.value = result.error
      }
    }

    return {
      email,
      password,
      error,
      rememberMe,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  background-color: #ffffff;
  padding: 2rem 0;
}

.login-card {
  background-color: #ffffff;
  border: 1px solid #000000;
  padding: 3rem;
}

.login-title {
  color: #000000;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #000000;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  color: #000000;
  font-weight: 500;
  margin-bottom: 0.5rem;
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
  padding-left: 45px;
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  height: 50px;
}

.input-wrapper .form-control:focus {
  background-color: #ffffff;
  border-color: #000000;
  color: #000000;
  outline: none;
}

.checkbox-label {
  display: flex;
  align-items: center;
  color: #000000;
  cursor: pointer;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.forgot-password {
  color: #000000;
  text-decoration: underline;
  font-size: 0.9rem;
}

.forgot-password:hover {
  color: #000000;
  text-decoration: underline;
}

.btn-login {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  height: 50px;
  font-size: 1.1rem;
  font-weight: bold;
}

.btn-login:hover {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
}

.register-link {
  color: #000000;
}

.register-link a {
  color: #000000;
  font-weight: bold;
  text-decoration: underline;
}

.register-link a:hover {
  color: #000000;
  text-decoration: underline;
}

.alert-danger {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
}
</style>
