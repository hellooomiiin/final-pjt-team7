<template>
  <div class="profile-emotions-container">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button @click="$router.push('/profile')" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
        <h2 class="page-title">나의 무드 & 영화 기록</h2>
        <div style="width: 100px;"></div> </div>

      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-else-if="historyList.length === 0" class="alert alert-info empty-state">
        <h4>아직 기록이 없습니다.</h4>
        <p>오늘의 기분에 맞춰 첫 번째 영화 추천을 받아보세요!</p>
        <button @click="$router.push('/')" class="btn btn-dark mt-3">
          영화 추천 받으러 가기
        </button>
      </div>

      <div v-else class="history-list">
        <div v-for="record in historyList" :key="record.id" class="history-card mb-5">
          
          <div class="history-header d-flex justify-content-between align-items-center mb-3">
            <div class="date-badge">
              {{ formatDate(record.created_at) }}
            </div>
            <div class="mood-badge" :class="record.mood">
              {{ getMoodLabel(record.mood) }}
            </div>
          </div>

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
              <p class="movie-title text-truncate">{{ movie.title }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // Auth 스토어 import

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
        'happy': '😊 행복', // 혹시 추가될 경우 대비
        'excited': '😆 신남'
      }
      return labels[mood] || mood
    }

    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.jpg'
      return `https://image.tmdb.org/t/p/w200${path}` // 작은 사이즈(w200) 사용
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
.profile-emotions-container {
  min-height: calc(100vh - 80px);
  padding: 3rem 0;
  background-color: #fff;
}

.page-title {
  font-weight: bold;
  text-align: center;
}

.loading-spinner {
  padding: 5rem 0;
}

/* --- 버튼 스타일 --- */
.btn-outline-secondary {
  border: 1px solid #000000;
  color: #000000;
  background-color: #ffffff;
  padding: 0.5rem 1rem;
  transition: all 0.2s;
}

.btn-outline-secondary:hover {
  background-color: #000000;
  color: #ffffff;
}

/* --- 기록 카드 스타일 --- */
.history-card {
  border: 1px solid #000;
  padding: 1.5rem;
  background-color: #fff;
  /* box-shadow: 5px 5px 0px rgba(0,0,0,0.1); 약간의 입체감 */
}

.history-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.date-badge {
  font-size: 0.95rem;
  font-weight: bold;
  color: #555;
}

.mood-badge {
  font-weight: bold;
  font-size: 1.1rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  border: 1px solid #000;
  background-color: #fff;
}

/* 기분별 색상 포인트 (선택사항) */
.mood-badge.sad { color: #0d6efd; border-color: #0d6efd; }
.mood-badge.angry { color: #dc3545; border-color: #dc3545; }
.mood-badge.bored { color: #6c757d; border-color: #6c757d; }

/* --- 영화 목록 (가로 배치) --- */
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
  background-color: #ccc;
  border-radius: 3px;
}

.movie-mini-card {
  width: 120px;
  flex-shrink: 0; /* 줄어들지 않게 고정 */
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
  border: 1px solid #ddd;
  margin-bottom: 0.5rem;
}

.movie-title {
  font-size: 0.85rem;
  margin: 0;
  color: #333;
}

/* --- 빈 상태 --- */
.empty-state {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 4rem 2rem;
  text-align: center;
}
</style>