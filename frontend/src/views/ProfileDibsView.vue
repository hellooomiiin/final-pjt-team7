<template>
  <div class="reviews-container" v-if="!loading && !error">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/profile')" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 헤더 -->
      <div class="reviews-header">
        <h3 class="reviews-title">내가 찜한 영화 ({{ dibsList.length }})</h3>
      </div>

      <!-- 영화 목록 -->
      <div v-if="dibsList.length > 0" class="movies-grid">
        <div 
          v-for="movie in dibsList" 
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
            <div class="heart-badge">❤️</div>
          </div>
          
          <div class="movie-info">
            <h5 class="movie-title">{{ movie.title }}</h5>
            <div class="movie-details">
              <span class="rating">★ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</span>
              <small class="year">{{ movie.release_date ? movie.release_date.split('-')[0] : '' }}</small>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-reviews">
        <p>아직 찜한 영화가 없습니다.</p>
        <p>마음에 드는 영화를 발견하면 하트(❤️)를 눌러보세요!</p>
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
  name: 'ProfileDibsView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const dibsList = ref([])
    const loading = ref(true)
    const error = ref(null)

    // 1. 찜한 목록 가져오기
    const fetchDibs = async () => {
      loading.value = true
      error.value = null
      
      const token = authStore.token
      if (!token) {
        alert('로그인이 필요합니다.')
        router.push('/login')
        return
      }

      try {
        // 백엔드에서 구현한 '내가 찜한 영화' API 호출
        const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/my-likes/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        dibsList.value = response.data
      } catch (err) {
        console.error('찜 목록 로드 실패:', err)
        error.value = '목록을 불러오는 중 문제가 발생했습니다.'
      } finally {
        loading.value = false
      }
    }

    // 2. 헬퍼 함수들
    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.jpg'
      return `https://image.tmdb.org/t/p/w300${path}` // 적당한 크기(w300)
    }

    const goToDetail = (id) => {
      router.push(`/movies/${id}`)
    }

    onMounted(() => {
      fetchDibs()
    })

    return {
      dibsList,
      loading,
      error,
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
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.heart-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  filter: drop-shadow(0 0 2px rgba(0,0,0,0.5));
}

.movie-info {
  padding: 1rem;
}

.movie-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  color: #ffffff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rating {
  color: #ffc107;
  font-weight: bold;
}

.year {
  color: #999999;
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
