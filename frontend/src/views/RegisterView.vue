<template>
  <div class="register-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="register-card">
            <h2 class="register-title">회원가입</h2>
            <p class="register-subtitle">Mood-Match와 함께 시작하세요</p>
            <form @submit.prevent="handleRegister">
              <div class="form-group mb-3">
                <label for="username" class="form-label">이름</label>
                <div class="input-wrapper">
                  <span class="input-icon">👤</span>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    v-model="formData.username"
                    placeholder="이름을 입력하세요"
                    required
                  />
                </div>
              </div>
              <div class="form-group mb-3">
                <label for="nickname" class="form-label">닉네임</label>
                <div class="input-wrapper">
                  <span class="input-icon">👤</span>
                  <input
                    type="text"
                    class="form-control"
                    id="nickname"
                    v-model="formData.nickname"
                    placeholder="닉네임을 입력하세요"
                    required
                  />
                </div>
              </div>
              <div class="form-group mb-3">
                <label for="email" class="form-label">이메일</label>
                <div class="input-wrapper">
                  <span class="input-icon">✉️</span>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="formData.email"
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
                    v-model="formData.password"
                    placeholder="********"
                    required
                  />
                </div>
              </div>
              <div class="form-group mb-4">
                <label for="password_confirm" class="form-label">비밀번호 확인</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    type="password"
                    class="form-control"
                    id="password_confirm"
                    v-model="formData.password_confirm"
                    placeholder="********"
                    required
                  />
                </div>
              </div>
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              <button type="submit" class="btn btn-register w-100 mb-3">
                회원가입
              </button>
              <div class="text-center login-link">
                <span>이미 계정이 있으신가요? </span>
                <router-link to="/login">로그인</router-link>
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
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const formData = ref({
      username: '',
      nickname: '',
      email: '',
      password: '',
      password_confirm: ''
    })
    const error = ref('')

    const handleRegister = async () => {
      error.value = ''
      const result = await authStore.register(formData.value)
      
      if (result.success) {
        router.push('/')
      } else {
        if (typeof result.error === 'object') {
          error.value = Object.values(result.error).flat().join(', ')
        } else {
          error.value = result.error
        }
      }
    }

    return {
      formData,
      error,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  background-color: #ffffff;
  padding: 2rem 0;
}

.register-card {
  background-color: #ffffff;
  border: 1px solid #000000;
  padding: 3rem;
}

.register-title {
  color: #000000;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.register-subtitle {
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

.btn-register {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  height: 50px;
  font-size: 1.1rem;
  font-weight: bold;
}

.btn-register:hover {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
}

.login-link {
  color: #000000;
}

.login-link a {
  color: #000000;
  font-weight: bold;
  text-decoration: underline;
}

.login-link a:hover {
  color: #000000;
  text-decoration: underline;
}

.alert-danger {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
}
</style>
