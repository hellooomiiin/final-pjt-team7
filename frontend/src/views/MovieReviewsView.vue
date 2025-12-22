<template>
  <div class="movie-reviews-container">
    <div class="container">
      <!-- 뒤로가기 버튼 -->
      <div class="mb-4">
        <button @click="$router.back()" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- 영화 정보 및 리뷰 목록 -->
      <div v-else-if="movie">
        <!-- 영화 정보 헤더 -->
        <div class="movie-header mb-4">
          <div class="row align-items-center">
            <div class="col-md-2">
              <img
                :src="movie.poster_path || '/placeholder.jpg'"
                class="movie-poster"
                :alt="movie.title"
              />
            </div>
            <div class="col-md-10">
              <h1 class="movie-title">{{ movie.title }}</h1>
              <p v-if="movie.original_title" class="movie-original-title">
                {{ movie.original_title }}
              </p>
            </div>
          </div>
        </div>

        <!-- 정렬 필터 -->
        <div class="filter-section mb-4">
          <div class="d-flex justify-content-between align-items-center">
            <h2 class="section-title mb-0">리뷰 목록 ({{ reviews.length }}개)</h2>
            <select v-model="sortOrder" @change="handleSortChange" class="form-select sort-select">
              <option value="-created_at">최신 순</option>
              <option value="created_at">오래된 순</option>
              <option value="-like_count">좋아요 순</option>
              <option value="-rating">높은 평가 순</option>
              <option value="rating">낮은 평가 순</option>
            </select>
          </div>
        </div>

        <!-- 리뷰 목록 -->
        <div v-if="reviewsLoading" class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else-if="reviews.length === 0" class="alert alert-info">
          아직 리뷰가 없습니다.
        </div>
        <div v-else class="reviews-list">
          <div
            v-for="review in reviews"
            :key="review.id"
            class="card mb-3 review-card"
          >
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title mb-0">{{ review.title }}</h5>
                <span class="badge bg-primary">평점: {{ review.rating }}/5</span>
              </div>
              <p class="card-text">{{ review.content }}</p>
              <div class="d-flex justify-content-between align-items-center mt-3">
                <small class="text-muted">
                  작성자: {{ review.user?.nickname || '익명' }} | 
                  작성일: {{ formatDate(review.created_at) }}
                </small>
                <button
                  @click="toggleLike(review)"
                  class="btn btn-sm"
                  :class="review.is_liked ? 'btn-danger' : 'btn-outline-danger'"
                  :disabled="likeLoading"
                >
                  <span v-if="review.is_liked">❤️</span>
                  <span v-else>🤍</span>
                  좋아요 ({{ review.like_count || 0 }})
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 영화 정보 없음 -->
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
  name: 'MovieReviewsView',
  setup() {
    const route = useRoute()
    const movie = ref(null)
    const reviews = ref([])
    const loading = ref(true)
    const reviewsLoading = ref(true)
    const likeLoading = ref(false)
    const sortOrder = ref('-created_at') // 기본값: 최신순

    // 영화 상세 정보 조회
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

    // 리뷰 목록 조회
    const fetchReviews = async () => {
      if (!movie.value) return
      
      reviewsLoading.value = true
      try {
        const response = await mockApi.getReviews({ 
          movie: movie.value.id,
          ordering: sortOrder.value
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

    // 정렬 변경 핸들러
    const handleSortChange = () => {
      fetchReviews()
    }

    // 좋아요 토글
    const toggleLike = async (review) => {
      if (likeLoading.value) return
      
      likeLoading.value = true
      try {
        // TODO: 실제 API 호출로 대체
        // const api = (await import('@/api')).default
        // if (review.is_liked) {
        //   await api.delete(`/reviews/${review.id}/like/`)
        // } else {
        //   await api.post(`/reviews/${review.id}/like/`)
        // }
        
        // 모킹: 로컬 상태만 업데이트
        review.is_liked = !review.is_liked
        review.like_count = review.is_liked 
          ? (review.like_count || 0) + 1 
          : Math.max(0, (review.like_count || 0) - 1)
      } catch (error) {
        console.error('좋아요 처리 실패:', error)
      } finally {
        likeLoading.value = false
      }
    }

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

    onMounted(async () => {
      await fetchMovieDetail()
      if (movie.value) {
        await fetchReviews()
      }
    })

    return {
      movie,
      reviews,
      loading,
      reviewsLoading,
      likeLoading,
      sortOrder,
      handleSortChange,
      toggleLike,
      formatDate
    }
  }
}
</script>

<style scoped>
.movie-reviews-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}

.loading-spinner {
  padding: 5rem 0;
}

.movie-header {
  padding: 2rem 0;
  border-bottom: 1px solid #000000;
}

.movie-poster {
  width: 100%;
  max-width: 150px;
  height: auto;
  border: 1px solid #000000;
}

.movie-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0.5rem;
}

.movie-original-title {
  font-size: 1.2rem;
  color: #666666;
  margin-bottom: 0;
}

.filter-section {
  padding: 1.5rem 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #000000;
}

.sort-select {
  max-width: 200px;
  border: 1px solid #000000;
  color: #000000;
  background-color: #ffffff;
}

.sort-select:focus {
  border-color: #000000;
  box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25);
}

.reviews-list {
  margin-top: 2rem;
}

.review-card {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  transition: transform 0.2s, box-shadow 0.2s;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #000000;
}

.card-text {
  color: #000000;
  line-height: 1.6;
  margin-bottom: 0;
}

.alert-info {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 2rem;
  text-align: center;
  margin-top: 2rem;
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

.btn-outline-danger {
  border: 1px solid #dc3545;
  color: #dc3545;
  background-color: #ffffff;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #ffffff;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
  color: #ffffff;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
}

@media (max-width: 768px) {
  .movie-title {
    font-size: 1.5rem;
  }
  
  .movie-poster {
    margin-bottom: 1rem;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-section .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
  
  .sort-select {
    width: 100%;
    max-width: none;
  }
}
</style>
