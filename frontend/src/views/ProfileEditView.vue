<template>
  <div class="profile-edit-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="edit-card">
            <div class="mb-4">
              <button @click="$router.push('/profile')" class="btn btn-back">
                ← 뒤로가기
              </button>
            </div>
            <h2 class="edit-title">회원정보 수정</h2>
            <p class="edit-subtitle">프로필 정보를 수정하세요</p>
            
            <form @submit.prevent="handleUpdate">
              <!-- 닉네임 -->
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

              <!-- 프로필 이미지 -->
              <div class="form-group mb-3">
                <label for="profile_image" class="form-label">프로필 이미지</label>
                <div class="image-upload-wrapper">
                  <input
                    type="file"
                    class="form-control-file"
                    id="profile_image"
                    accept="image/*"
                    @change="handleImageChange"
                  />
                  <p class="image-hint">새 이미지를 선택하세요 (선택사항)</p>
                  <div v-if="previewImage" class="image-preview">
                    <img :src="previewImage" alt="프로필 미리보기" />
                  </div>
                </div>
              </div>

              <!-- 새 비밀번호 (선택) -->
              <div class="form-group mb-3">
                <label for="new_password" class="form-label">새 비밀번호 (선택사항)</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    type="password"
                    class="form-control"
                    id="new_password"
                    v-model="formData.new_password"
                    placeholder="비밀번호를 변경하려면 입력하세요"
                  />
                </div>
              </div>

              <!-- 새 비밀번호 확인 -->
              <div class="form-group mb-4" v-if="formData.new_password">
                <label for="password_confirm" class="form-label">새 비밀번호 확인</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    type="password"
                    class="form-control"
                    id="password_confirm"
                    v-model="formData.password_confirm"
                    placeholder="비밀번호를 다시 입력하세요"
                  />
                </div>
              </div>

              <!-- 에러 메시지 -->
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <!-- 성공 메시지 -->
              <div v-if="success" class="alert alert-success" role="alert">
                회원정보가 수정되었습니다.
              </div>

              <!-- 제출 버튼 -->
              <button 
                type="submit" 
                class="btn btn-update w-100 mb-3"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ loading ? '수정 중...' : '수정 완료' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ProfileEditView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const loading = ref(false)
    const error = ref('')
    const success = ref(false)
    const previewImage = ref(null)
    const selectedImage = ref(null)

    const formData = ref({
      nickname: '',
      new_password: '',
      password_confirm: ''
    })

    // 기존 사용자 정보 로드
    const loadUserData = () => {
      if (authStore.user) {
        formData.value.nickname = authStore.user.nickname || ''
      }
    }

    // 이미지 선택 핸들러
    const handleImageChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedImage.value = file
        // 미리보기 생성
        const reader = new FileReader()
        reader.onload = (e) => {
          previewImage.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    // 회원정보 수정 핸들러
    const handleUpdate = async () => {
      error.value = ''
      success.value = false
      loading.value = true

      try {
        // 비밀번호 확인 검증
        if (formData.value.new_password && formData.value.new_password !== formData.value.password_confirm) {
          error.value = '새 비밀번호가 일치하지 않습니다.'
          loading.value = false
          return
        }

        // FormData 생성 (이미지 파일이 있을 수 있으므로)
        const updateData = new FormData()
        updateData.append('nickname', formData.value.nickname)
        
        if (selectedImage.value) {
          updateData.append('profile_image', selectedImage.value)
        }
        
        if (formData.value.new_password) {
          updateData.append('new_password', formData.value.new_password)
          updateData.append('password_confirm', formData.value.password_confirm)
        }

        // API 호출
        const api = (await import('@/api')).default
        const response = await api.patch('/accounts/profile/update/', updateData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        // 성공 시 사용자 정보 업데이트
        if (response.data) {
          authStore.user = response.data
          success.value = true
          
          // 프로필 정보 다시 불러오기
          await authStore.fetchProfile()
          
          // 2초 후 프로필 페이지로 이동
          setTimeout(() => {
            router.push('/profile')
          }, 1500)
        }
      } catch (err) {
        console.error('회원정보 수정 에러:', err)
        
        // 에러 메시지 처리
        let errorMessage = '회원정보 수정에 실패했습니다.'
        
        if (err.response?.data) {
          const errorData = err.response.data
          
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
        } else if (err.message) {
          errorMessage = err.message
        }
        
        error.value = errorMessage
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      // 로그인 확인
      if (!authStore.isAuthenticated) {
        router.push('/login')
        return
      }
      
      // 사용자 정보 로드
      loadUserData()
    })

    return {
      formData,
      loading,
      error,
      success,
      previewImage,
      handleImageChange,
      handleUpdate
    }
  }
}
</script>

<style scoped>
.profile-edit-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  background-color: #ffffff;
  padding: 2rem 0;
}

.edit-card {
  background-color: #ffffff;
  border: 1px solid #000000;
  padding: 3rem;
}

.btn-back {
  border: 1px solid #000000;
  color: #000000;
  background-color: #ffffff;
  padding: 0.5rem 1rem;
  text-decoration: none;
  cursor: pointer;
}

.btn-back:hover {
  background-color: #000000;
  color: #ffffff;
}

.edit-title {
  color: #000000;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  margin-top: 1rem;
}

.edit-subtitle {
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
  box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25);
}

.image-upload-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-control-file {
  padding: 0.5rem;
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
}

.image-hint {
  color: #666666;
  font-size: 0.9rem;
  margin: 0;
}

.image-preview {
  margin-top: 1rem;
}

.image-preview img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border: 1px solid #000000;
  border-radius: 8px;
}

.btn-update {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  height: 50px;
  font-size: 1.1rem;
  font-weight: bold;
}

.btn-update:hover:not(:disabled) {
  border: 1px solid #000000;
  background-color: #000000;
  color: #ffffff;
}

.btn-update:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert-danger {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #dc3545;
}

.alert-success {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #28a745;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.2em;
}

@media (max-width: 768px) {
  .edit-card {
    padding: 2rem;
  }

  .edit-title {
    font-size: 1.5rem;
  }
}
</style>
