<template>
  <div class="reviews-container">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/profile')" class="back-button">
        ← 뒤로가기
      </button>

      <div class="edit-card">
        <h2 class="edit-title">회원정보 수정</h2>
        <p class="edit-subtitle">프로필 정보를 수정하세요</p>
        
        <form @submit.prevent="handleUpdate">
          <!-- 닉네임 -->
          <div class="form-group">
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
          <div class="form-group">
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
          <div class="form-group">
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
          <div class="form-group" v-if="formData.new_password">
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
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <!-- 성공 메시지 -->
          <div v-if="success" class="alert alert-success">
            회원정보가 수정되었습니다.
          </div>

          <!-- 제출 버튼 -->
          <button 
            type="submit" 
            class="btn-update"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
            {{ loading ? '수정 중...' : '수정 완료' }}
          </button>
        </form>
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

/* 뒤로가기 버튼 */
.back-button {
  background: none;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  color: #999999;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
  transition: color 0.2s;
}

.back-button:hover {
  color: #ffffff;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.back-button:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.back-button:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.edit-card {
  background-color: #1a1a1a;
  padding: 22px;
  border-radius: 8px;
}

.edit-title {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  margin-top: 0;
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
  padding-left: 45px;
  background-color: #333333;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  height: 50px;
  border-radius: 4px;
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

.image-upload-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-control-file {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background-color: #333333;
  color: #ffffff;
  border-radius: 4px;
}

.image-hint {
  color: #999999;
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
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.btn-update {
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
  margin-top: 1rem;
}

.btn-update:hover:not(:disabled) {
  background-color: #252525;
  color: #ffffff;
}

.btn-update:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert-danger {
  background-color: #1a1a1a;
  border: 1px solid rgba(220, 53, 69, 0.5);
  color: #dc3545;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.alert-success {
  background-color: #1a1a1a;
  border: 1px solid rgba(40, 167, 69, 0.5);
  color: #28a745;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.2em;
}

@media (max-width: 768px) {
  .reviews-wrapper {
    padding: 0 0.5rem;
  }

  .edit-card {
    padding: 1.5rem;
  }

  .edit-title {
    font-size: 1.5rem;
  }
}
</style>
