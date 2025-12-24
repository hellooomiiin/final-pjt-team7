<template>
  <div class="profile-dibs-container">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button @click="$router.push('/profile')" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
        <h2 class="page-title">내가 찜한 영화 ({{ dibsList.length }})</h2>
        <div style="width: 100px;"></div> </div>

      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-else-if="dibsList.length === 0" class="alert alert-info empty-state">
        <h4>아직 찜한 영화가 없습니다.</h4>
        <p>마음에 드는 영화를 발견하면 하트(❤️)를 눌러보세요!</p>
        <button @click="$router.push('/')" class="btn btn-dark mt-3">
          영화 둘러보러 가기
        </button>
      </div>

      <div v-else class="movies-grid">
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
            <h5 class="movie-title text-truncate">{{ movie.title }}</h5>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <span class="rating">★ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</span>
              <small class="text-muted">{{ movie.release_date ? movie.release_date.split('-')[0] : '' }}</small>
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
.profile-dibs-container {
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

/* --- 영화 그리드 레이아웃 --- */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  padding-top: 1rem;
}

/* --- 영화 카드 스타일 --- */
.movie-card {
  border: 1px solid #000;
  background-color: #fff;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 5px 5px 0px rgba(0,0,0,0.1);
}

.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3; /* 포스터 비율 고정 */
  overflow: hidden;
  border-bottom: 1px solid #000;
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
  margin-bottom: 0;
}

.rating {
  color: #ffc107; /* 별점 색상 */
  font-weight: bold;
  text-shadow: 1px 1px 0px #000; /* 가독성 위한 테두리 효과 */
  -webkit-text-stroke: 0.5px #000;
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