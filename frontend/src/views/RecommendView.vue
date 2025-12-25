<template>
  <div class="reviews-container" v-if="!loading">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/')" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 헤더 -->
      <div class="reviews-header">
        <h3 class="reviews-title">{{ moodMessage }}</h3>
        <p class="reviews-subtitle">이런 영화들이 기분에 도움이 될 거예요!</p>
      </div>

      <!-- 영화 목록 -->
      <div v-if="recommendedMovies.length > 0" class="movies-grid">
        <div 
          v-for="movie in recommendedMovies" 
          :key="movie.tmdb_id" 
          class="movie-card"
          @click="goToDetail(movie.tmdb_id)"
        >
          <div class="poster-wrapper">
            <img 
              :src="getImageUrl(movie.poster_path)" 
              :alt="movie.title" 
              class="movie-poster"
            />
          </div>
          <div class="movie-info">
            <h5 class="movie-title">{{ movie.title }}</h5>
            <span class="rating">★ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</span>
          </div>
        </div>
      </div>

      <div v-else class="no-reviews">
        <p>추천 영화를 불러오는 중입니다.</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

// auth.js에 정의된 스토어 가져오기
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'RecommendView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 스토어 초기화
    const authStore = useAuthStore()

    const loading = ref(true)
    const recommendedMovies = ref([])

    const currentMood = computed(() => route.query.mood)

    const moodMessage = computed(() => {
      switch(currentMood.value) {
        case 'bored': return '🥱 심심할 땐, 시간 순삭 영화!';
        case 'angry': return '😡 화날 땐, 다 때려부수는 액션!';
        case 'sad': return '😢 슬플 땐, 실컷 울 수 있는 영화!';
        default: return '추천 영화 목록';
      }
    })

    const fetchRecommendations = async () => {
      loading.value = true
      
      //  토큰 가져오기
      const token = authStore.token 
      
      if (!token) {
        alert('로그인이 필요한 서비스입니다.')
        router.push('/login')
        return
      }

      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/api/v1/recommends/generate/',
          { mood: currentMood.value },
          {
            headers: {
              //
              Authorization: `Bearer ${token}` 
            }
          }
        )
        
        recommendedMovies.value = response.data

      } catch (err) {
        console.error('추천 영화 생성 실패:', err)
        if (err.response && err.response.status === 401) {
          alert('인증 정보가 만료되었습니다. 다시 로그인해주세요.')
          // [추가] 토큰 만료 시 스토어의 로그아웃 함수 실행해서 정리해주면 좋음
          authStore.logout() 
          router.push('/login')
        }
      } finally {
        loading.value = false
      }
    }

    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.jpg'
      return `https://image.tmdb.org/t/p/w500${path}`
    }

    const goToDetail = (id) => {
      router.push(`/movies/${id}`)
    }

    onMounted(() => {
      if (!currentMood.value) {
        alert('잘못된 접근입니다.')
        router.push('/')
        return
      }
      fetchRecommendations()
    })

    return {
      moodMessage,
      recommendedMovies,
      loading,
      goToDetail,
      getImageUrl
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
  margin-bottom: 2rem;
}

.reviews-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.reviews-subtitle {
  font-size: 1rem;
  color: #999999;
  margin: 0;
}

/* 영화 그리드 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  padding-top: 1rem;
}

/* 영화 카드 */
.movie-card {
  background-color: #1a1a1a;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  overflow: hidden;
}

.movie-card:hover {
  background-color: #252525;
}

.poster-wrapper {
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  padding: 1rem;
  text-align: center;
}

.movie-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rating {
  color: #ffc107;
  font-weight: bold;
  font-size: 0.9rem;
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

  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>
