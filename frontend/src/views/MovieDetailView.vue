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
            <h3 class="section-title">리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }})</h3>
            
            <router-link 
              :to="{ name: 'movie-reviews', params: { id: movie.id } }" 
              class="btn btn-outline-secondary"
            >
              전체보기 →
            </router-link>
          </div>
          <div v-if="reviewsLoading" class="text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-if="!movie.review_set || movie.review_set.length === 0" class="alert alert-info">
            아직 리뷰가 없습니다. 첫 리뷰를 작성해보세요!
          </div>
          <div v-else>
            <div
              v-for="review in movie.review_set.slice(0, 3)"
              :key="review.id"
              class="card mb-3 hover-effect"
              style="cursor: pointer;"
              @click="$router.push({ name: 'review-detail', params: { id: movie.id, reviewId: review.id } })"
            >
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <h5 class="card-title text-truncate" style="max-width: 70%;">
                    {{ review.title }} 
                  </h5>
                  <span class="badge bg-warning text-dark align-self-start">★ {{ review.rank }}</span>
                </div>
                
                <p class="card-text text-truncate text-muted my-2">{{ review.content }}</p>
                
                <div class="d-flex justify-content-between align-items-center mt-3">
                  <small class="text-muted">
                    by {{ review.user }} | {{ new Date(review.created_at).toLocaleDateString() }}
                  </small>
                  
                  <div class="d-flex gap-3 text-secondary small">
                    <span>
                      ❤ {{ review.like_count || 0 }}
                    </span>
                    <span>
                      💬 {{ review.comments ? review.comments.length : 0 }}
                    </span>
                  </div>
                </div>

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

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // ★ 스토어 가져오기
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore() // ★ 스토어 사용

const movie = ref(null)
const loading = ref(true) // 로딩 상태 추가

const getMovieDetail = async () => {
  loading.value = true
  try {
    const res = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`,
      headers: {
        // ★ [핵심] 상세 페이지도 토큰을 'Bearer'로 보내야 리뷰(review_set)를 줍니다!
        Authorization: `Bearer ${store.token}` 
      }
    })
    
    movie.value = res.data
    console.log('영화 데이터 확인:', res.data) // 콘솔에서 review_set이 들어있는지 확인해보세요!

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 날짜 예쁘게 바꾸는 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  getMovieDetail()
})
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

