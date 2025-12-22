<template>
  <div class="movie-detail-container">
    <div class="container">
      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else-if="movie" class="movie-detail">
        <div class="row">
          <div class="col-md-4">
            <img
              :src="movie.poster_path || '/placeholder.jpg'"
              class="movie-poster-large"
              :alt="movie.title"
            />
          </div>
          <div class="col-md-8">
            <h1 class="movie-title">{{ movie.title }}</h1>
            <p v-if="movie.original_title" class="movie-original-title">
              {{ movie.original_title }}
            </p>
            <div class="movie-info">
              <p v-if="movie.overview" class="movie-overview">{{ movie.overview }}</p>
              <div class="movie-meta">
                <span v-if="movie.release_date" class="meta-item">
                  개봉일: {{ movie.release_date }}
                </span>
                <span v-if="movie.vote_average" class="meta-item">
                  평점: {{ movie.vote_average }}/10
                </span>
                <span v-if="movie.popularity" class="meta-item">
                  인기도: {{ movie.popularity }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 리뷰 섹션 -->
        <div v-if="movie" class="reviews-section mt-5">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="section-title">리뷰</h3>
            <router-link 
              :to="`/movies/${movie.id}/reviews`" 
              class="btn btn-outline-secondary"
            >
              더보기 →
            </router-link>
          </div>
          <div v-if="reviewsLoading" class="text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-else-if="reviews.length === 0" class="alert alert-info">
            아직 리뷰가 없습니다.
          </div>
          <div v-else>
            <div
              v-for="review in reviews.slice(0, 3)"
              :key="review.id"
              class="card mb-3"
            >
              <div class="card-body">
                <h5 class="card-title">{{ review.title }}</h5>
                <p class="card-text">{{ review.content }}</p>
                <div class="mb-2">
                  <span class="badge bg-primary me-2">평점: {{ review.rating }}/5</span>
                </div>
                <small class="text-muted">
                  작성자: {{ review.user.nickname }} | 
                  작성일: {{ formatDate(review.created_at) }}
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="alert alert-info">
        영화 정보를 찾을 수 없습니다.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { mockApi } from '@/data/mockData'

export default {
  name: 'MovieDetailView',
  setup() {
    const route = useRoute()
    const movie = ref(null)
    const loading = ref(true)
    const reviews = ref([])
    const reviewsLoading = ref(true)

    const fetchMovieDetail = async () => {
      try {
        const movieId = route.params.id
        const response = await mockApi.getMovieDetail(movieId)
        movie.value = response.data
      } catch (error) {
        console.error('영화 상세 정보 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchReviews = async () => {
      if (!movie.value) return
      
      reviewsLoading.value = true
      try {
        const response = await mockApi.getReviews({ 
          movie: movie.value.id,
          ordering: '-created_at' // 최신순 정렬
        })
        if (response.data.results) {
          reviews.value = response.data.results
        } else {
          reviews.value = response.data || []
        }
      } catch (error) {
        console.error('리뷰 로드 실패:', error)
      } finally {
        reviewsLoading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    onMounted(async () => {
      await fetchMovieDetail()
      if (movie.value) {
        await fetchReviews()
      }
    })

    return {
      movie,
      loading,
      reviews,
      reviewsLoading,
      formatDate
    }
  }
}
</script>

<style scoped>
.movie-detail-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}

.loading-spinner {
  padding: 5rem 0;
}

.movie-detail {
  margin-top: 2rem;
}

.movie-poster-large {
  width: 100%;
  max-width: 400px;
  height: auto;
  border: 1px solid #000000;
}

.movie-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0.5rem;
}

.movie-original-title {
  font-size: 1.2rem;
  color: #666666;
  margin-bottom: 2rem;
}

.movie-overview {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #000000;
  margin-bottom: 2rem;
}

.movie-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 2rem;
}

.meta-item {
  font-size: 1rem;
  color: #000000;
  padding: 0.5rem 1rem;
  border: 1px solid #000000;
  background-color: #ffffff;
}

.alert-info {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 2rem;
  text-align: center;
  margin-top: 3rem;
}

.reviews-section {
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 1px solid #000000;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0;
}

.card {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
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
  .movie-title {
    font-size: 1.8rem;
  }
  
  .movie-poster-large {
    margin-bottom: 2rem;
  }
  
  .movie-meta {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>

