<template>
  <div class="profile-container">
    <div class="container">
      <!-- 뒤로가기 버튼 -->
      <div class="mb-4">
        <button @click="$router.push('/')" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- 프로필 정보 및 메뉴 -->
      <div v-else-if="user" class="profile-content">
        <!-- 프로필 헤더 -->
        <div class="profile-header mb-5">
          <h1 class="profile-title">프로필</h1>
          <div class="profile-info">
            <div class="profile-avatar">
              <img 
                v-if="user.profile_image" 
                :src="getImageUrl(user.profile_image)" 
                alt="프로필 이미지"
                class="avatar-image"
              />
              <span v-else class="avatar-icon">👤</span>
            </div>
            <div class="profile-details">
              <h2 class="profile-nickname">{{ user.nickname || '닉네임 없음' }}</h2>
              <p class="profile-email">{{ user.email }}</p>
              <p v-if="user.created_at" class="profile-date">
                가입일: {{ formatDate(user.created_at) }}
              </p>
            </div>
          </div>
        </div>

        <!-- 메뉴 버튼들 -->
        <div class="profile-menu">
          <h3 class="menu-title">메뉴</h3>
          <div class="menu-buttons">
            <router-link to="/profile/edit" class="menu-button">
              <span class="menu-icon">✏️</span>
              <span class="menu-text">회원정보 수정</span>
              <span class="menu-arrow">→</span>
            </router-link>
            <router-link to="/profile/emotions" class="menu-button">
              <span class="menu-icon">💭</span>
              <span class="menu-text">감정 분석 기록</span>
              <span class="menu-arrow">→</span>
            </router-link>
            <router-link to="/profile/reviews" class="menu-button">
              <span class="menu-icon">⭐</span>
              <span class="menu-text">리뷰</span>
              <span class="menu-arrow">→</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- 사용자 정보 없음 -->
      <div v-else class="alert alert-info">
        사용자 정보를 불러올 수 없습니다.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ProfileView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const loading = ref(true)

    const user = computed(() => authStore.user)

    // 날짜 포맷팅
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 이미지 URL 생성
    const getImageUrl = (imagePath) => {
      if (!imagePath) return null
      // 절대 URL이면 그대로 사용
      if (imagePath.startsWith('http')) return imagePath
      // 상대 경로면 백엔드 URL과 결합
      const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      return `${baseURL.replace('/api/v1', '')}/${imagePath}`
    }

    // 프로필 정보 불러오기
    const loadProfile = async () => {
      loading.value = true
      try {
        // 로그인 상태 확인
        if (!authStore.isAuthenticated) {
          router.push('/login')
          return
        }

        // 항상 최신 프로필 정보 가져오기
        await authStore.fetchProfile()
      } catch (error) {
        console.error('프로필 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadProfile()
    })

    return {
      user,
      loading,
      formatDate,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.profile-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}

.loading-spinner {
  padding: 5rem 0;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  padding: 2rem 0;
  border-bottom: 1px solid #000000;
}

.profile-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 2rem;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid #000000;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  flex-shrink: 0;
}

.avatar-icon {
  font-size: 3rem;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-details {
  flex: 1;
}

.profile-nickname {
  font-size: 1.5rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0.5rem;
}

.profile-email {
  font-size: 1rem;
  color: #666666;
  margin-bottom: 0.5rem;
}

.profile-date {
  font-size: 0.9rem;
  color: #888888;
  margin-bottom: 0;
}

.profile-menu {
  margin-top: 3rem;
}

.menu-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 1.5rem;
}

.menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.menu-button {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  text-decoration: none;
  transition: all 0.2s;
}

.menu-button:hover {
  background-color: #000000;
  color: #ffffff;
}

.menu-button-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.menu-button-disabled:hover {
  background-color: #ffffff;
  color: #000000;
}

.menu-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.menu-text {
  flex: 1;
  font-size: 1.1rem;
  font-weight: 500;
}

.menu-arrow {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.alert-info {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 2rem;
  text-align: center;
  margin-top: 3rem;
}

.btn-outline-secondary {
  border: 1px solid #000000;
  color: #000000;
  background-color: #ffffff;
}

.btn-outline-secondary:hover {
  background-color: #000000;
  color: #ffffff;
}

@media (max-width: 768px) {
  .profile-info {
    flex-direction: column;
    text-align: center;
  }

  .profile-title {
    font-size: 1.5rem;
  }

  .menu-button {
    padding: 1rem;
  }

  .menu-text {
    font-size: 1rem;
  }
}
</style>

