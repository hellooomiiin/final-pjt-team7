<template>
  <div class="home-container">
    <div class="container">
      <!-- Welcome Section -->
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">
            <span class="check-icon">✓</span>
            Mood-Match에 오신 것을 환영합니다
          </h1>
          <p class="welcome-subtitle">
            AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다
          </p>
        </div>
      </div>

      <!-- Popular Movies Section -->
      <div class="popular-movies-section">
        <h2 class="section-title">인기 영화</h2>
        <p class="section-subtitle">지금 가장 많이 찾는 영화들을 만나보세요</p>
        <div v-if="loading" class="text-center loading-spinner">
          <div class="spinner-border text-danger" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else class="movies-scroll-container">
          <div class="movies-grid">
            <div
              v-for="movie in popularMovies"
              :key="movie.id"
              class="movie-card-item"
              @click="goToMovieDetail(movie.id)"
            >
              <div class="movie-card">
                <img
                  :src="movie.poster_path || '/placeholder.jpg'"
                  class="movie-poster"
                  :alt="movie.title"
                />
              </div>
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
import { mockApi } from '@/data/mockData'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    const popularMovies = ref([])
    const loading = ref(true)

    const fetchPopularMovies = async () => {
      try {
        const response = await mockApi.getPopularMovies()
        popularMovies.value = response.data
      } catch (error) {
        console.error('인기 영화 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    const goToMovieDetail = (movieId) => {
      router.push(`/movies/${movieId}`)
    }

    onMounted(() => {
      fetchPopularMovies()
    })

    return {
      popularMovies,
      loading,
      goToMovieDetail
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}

.welcome-section {
  margin-bottom: 4rem;
  text-align: center;
}

.welcome-content {
  max-width: 800px;
  margin: 0 auto;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 1rem;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #000000;
  margin-bottom: 2rem;
}

.btn-recommend {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  text-decoration: none;
  display: inline-block;
}

.btn-recommend:hover {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
}

.popular-movies-section {
  margin-top: 4rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1rem;
  color: #000000;
  margin-bottom: 2rem;
}

.loading-spinner {
  padding: 3rem 0;
}

.movies-scroll-container {
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 1rem;
}

.movies-grid {
  display: flex;
  gap: 1.5rem;
  padding-bottom: 1rem;
}

.movie-card-item {
  flex-shrink: 0;
  width: 280px;
  cursor: pointer;
}

.movie-card {
  background-color: #ffffff;
  border: 1px solid #000000;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 400px;
  object-fit: cover;
  display: block;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 1.8rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .movie-card-item {
    width: 200px;
  }
  
  .movie-poster {
    height: 300px;
  }
}
</style>
