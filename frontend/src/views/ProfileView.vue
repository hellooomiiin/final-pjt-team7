<template>
  <div class="reviews-container" v-if="!loading">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/')" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 프로필 정보 및 메뉴 -->
      <div v-if="user" class="profile-content">
        <!-- 프로필 헤더 -->
        <div class="profile-header">
          <h1 class="profile-title">프로필</h1>
          <div class="profile-info">
            <div class="profile-avatar">
              <img 
                :src="getProfileImageUrl()" 
                alt="프로필 이미지"
                class="avatar-image"
              />
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
            <router-link to="/profile/dibs" class="menu-button">
              <span class="menu-icon">❤️</span>
              <span class="menu-text">찜</span>
              <span class="menu-arrow">→</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- 사용자 정보 없음 -->
      <div v-else class="no-reviews">
        <p>사용자 정보를 불러올 수 없습니다.</p>
      </div>
    </div>
  </div>
  <div v-else class="loading-container">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import noProfileImage from '@/assets/no-profile.png'

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
      if (!imagePath) return noProfileImage
      // 절대 URL이면 그대로 사용
      if (imagePath.startsWith('http')) return imagePath
      // 상대 경로면 백엔드 URL과 결합
      const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      return `${baseURL.replace('/api/v1', '')}/${imagePath}`
    }
    
    // 프로필 이미지 URL 생성 (프로필 이미지가 없으면 no-profile.png 사용)
    const getProfileImageUrl = () => {
      if (user.value?.profile_image) {
        return getImageUrl(user.value.profile_image)
      }
      return noProfileImage
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
      getImageUrl,
      getProfileImageUrl
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

.profile-content {
  width: 100%;
}

.profile-header {
  padding: 2rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
}

.profile-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
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
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #333333;
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
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.profile-email {
  font-size: 1rem;
  color: #999999;
  margin-bottom: 0.5rem;
}

.profile-date {
  font-size: 0.9rem;
  color: #999999;
  margin-bottom: 0;
}

.profile-menu {
  margin-top: 2rem;
}

.menu-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
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
  padding: 22px;
  background-color: #1a1a1a;
  color: #ffffff;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.menu-button:hover {
  background-color: #252525;
  color: #ffffff;
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

.no-reviews {
  text-align: center;
  padding: 3rem 0;
  color: #999999;
}

.loading-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #000000;
}

@media (max-width: 768px) {
  .reviews-wrapper {
    padding: 0 0.5rem;
  }

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
