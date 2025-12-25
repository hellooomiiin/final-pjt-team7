<template>
  <div class="reviews-container" v-if="!loading && !error">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/profile')" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 헤더 -->
      <div class="reviews-header">
        <h3 class="reviews-title">나의 무드 & 영화 기록</h3>
      </div>

      <!-- 기록 목록 -->
      <div v-if="historyList.length > 0" class="history-list">
        <div v-for="record in historyList" :key="record.id" class="history-card">
          <div class="history-header">
            <div class="date-badge">
              {{ formatDate(record.created_at) }}
            </div>
            <div class="mood-badge" :class="record.mood">
              {{ getMoodLabel(record.mood) }}
            </div>
          </div>

          <div class="card-divider"></div>

          <div class="movies-row">
            <div 
              v-for="movie in record.recommended_movies" 
              :key="movie.tmdb_id" 
              class="movie-mini-card"
              @click="goToDetail(movie.tmdb_id)"
            >
              <img 
                :src="getImageUrl(movie.poster_path)" 
                :alt="movie.title" 
                class="movie-poster"
              />
              <p class="movie-title">{{ movie.title }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-reviews">
        <p>아직 기록이 없습니다.</p>
        <p>오늘의 기분에 맞춰 첫 번째 영화 추천을 받아보세요!</p>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="loading-container">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div v-else-if="error" class="loading-container">
    <p class="text-danger">{{ error }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ProfileEmotionsView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const historyList = ref([])
    const loading = ref(true)
    const error = ref(null)

    // 1. 기록 데이터 가져오기
    const fetchHistory = async () => {
      loading.value = true
      error.value = null
      
      const token = authStore.token
      if (!token) {
        alert('로그인이 필요합니다.')
        router.push('/login')
        return
      }

      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/recommends/history/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        historyList.value = response.data
      } catch (err) {
        console.error('기록 로드 실패:', err)
        error.value = '기록을 불러오는 중 문제가 발생했습니다.'
      } finally {
        loading.value = false
      }
    }

    // 2. 헬퍼 함수들
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('ko-KR', {
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getMoodLabel = (mood) => {
      const labels = {
        'bored': '🥱 심심함',
        'angry': '😡 화남',
        'sad': '😢 슬픔',
        'happy': '😊 행복',
        'stressed': '🤯 스트레스'
      }
      return labels[mood] || mood
    }

    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.jpg'
      return `https://image.tmdb.org/t/p/w200${path}`
    }

    const goToDetail = (id) => {
      router.push(`/movies/${id}`)
    }

    onMounted(() => {
      fetchHistory()
    })

    return {
      historyList,
      loading,
      error,
      formatDate,
      getMoodLabel,
      getImageUrl,
      goToDetail
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

/* 헤더 */
.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.reviews-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
}

/* 기록 목록 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 기록 카드 */
.history-card {
  padding: 22px;
  background-color: #1a1a1a;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.history-card:hover {
  background-color: #252525;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.date-badge {
  font-size: 0.95rem;
  font-weight: bold;
  color: #ffffff;
}

.mood-badge {
  font-weight: bold;
  font-size: 1rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background-color: #333333;
  color: #ffffff;
}

.mood-badge.sad {
  color: #0d6efd;
  border-color: #0d6efd;
}

.mood-badge.angry {
  color: #dc3545;
  border-color: #dc3545;
}

.mood-badge.bored {
  color: #6c757d;
  border-color: #6c757d;
}

.mood-badge.happy {
  color: #28a745;
  border-color: #28a745;
}

.mood-badge.stressed {
  color: #ffc107;
  border-color: #ffc107;
}

.card-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 1rem 0;
}

/* 영화 목록 (가로 배치) */
.movies-row {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-top: 1rem;
  padding-bottom: 0.5rem;
}

.movies-row::-webkit-scrollbar {
  height: 6px;
}

.movies-row::-webkit-scrollbar-thumb {
  background-color: #666666;
  border-radius: 3px;
}

.movie-mini-card {
  width: 120px;
  flex-shrink: 0;
  cursor: pointer;
  text-align: center;
  transition: transform 0.2s;
}

.movie-mini-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.movie-title {
  font-size: 0.85rem;
  margin: 0;
  color: #ffffff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

/* 반응형 */
@media (max-width: 768px) {
  .reviews-wrapper {
    padding: 0 0.5rem;
  }

  .reviews-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
