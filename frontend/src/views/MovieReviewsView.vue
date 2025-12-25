<script setup>
import { ref, onMounted, computed } from 'vue' // ★ computed 추가
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import StarDisplay from '@/components/StarDisplay.vue'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const movie = ref(null)
const sortBy = ref('latest') // ★ 정렬 기준 (기본값: 최신순)

const isEdited = (created, updated) => {
  const createdTime = new Date(created).getTime()
  const updatedTime = new Date(updated).getTime()
  return updatedTime - createdTime > 2000 
}

const getMovieDetail = async () => {
  try {
    // route.params.id는 tmdb_id (MovieDetailView에서 movie.tmdb_id를 전달)
    // 영화 정보 가져오기 (토큰 없이도 조회 가능)
    const movieRes = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`
    })
    movie.value = movieRes.data
    
    // 영화의 DB id를 사용해서 리뷰 목록 가져오기 (토큰 없이도 조회 가능)
    const movieDbId = movie.value.id
    
    const reviewsRes = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
      params: { movie: movieDbId }
    })
    
    // review_set이 없으면 리뷰 목록 API에서 가져온 데이터로 추가
    if (!movie.value.review_set) {
      movie.value.review_set = reviewsRes.data.results || reviewsRes.data
    }
  } catch (err) {
    console.error(err)
  }
}

// ★ [핵심] 정렬된 리뷰 목록을 반환하는 computed 함수
const sortedReviews = computed(() => {
  if (!movie.value || !movie.value.review_set) return []

  // 원본 배열을 복사([...])해서 정렬해야 안전함
  const reviews = [...movie.value.review_set]

  if (sortBy.value === 'latest') {
    // 최신순 (날짜 내림차순)
    return reviews.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else if (sortBy.value === 'oldest') {
    // 오래된 순 (날짜 오름차순)
    return reviews.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  } else if (sortBy.value === 'highRank') {
    // 평가 높은순 (평점 내림차순)
    return reviews.sort((a, b) => b.rank - a.rank)
  } else if (sortBy.value === 'lowRank') {
    // 평가 낮은순 (평점 오름차순)
    return reviews.sort((a, b) => a.rank - b.rank)
  } else if (sortBy.value === 'likes') {
    // 좋아요 순 (좋아요 수 내림차순)
    return reviews.sort((a, b) => (b.like_count || 0) - (a.like_count || 0))
  }
  return reviews
})

const goDetail = (reviewId) => {
  router.push({ name: 'review-detail', params: { id: route.params.id, reviewId: reviewId } })
}

const goCreateReview = async () => {
  if (!movie.value) return
  
  try {
    // store.user가 없으면 fetchProfile로 최신 정보 가져오기
    if (!store.user) {
      await store.fetchProfile()
    }
    
    // movie.value.id는 DB의 id (Movie 모델의 PK)
    // Review 모델의 movie 필드는 Movie의 id를 참조하므로 movie.value.id 사용
    // API를 직접 호출해서 현재 사용자가 이미 이 영화에 리뷰를 작성했는지 확인
    const response = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
      params: {
        movie: movie.value.id
      },
      headers: { Authorization: `Bearer ${store.token}` }
    })
    
    const currentUsername = store.user?.username
    
    // 페이지네이션된 응답이므로 response.data.results 사용
    const reviews = response.data.results || response.data
    
    // 응답에서 현재 사용자가 작성한 리뷰가 있는지 확인
    const hasMyReview = Array.isArray(reviews) && reviews.some(
      review => review.user === currentUsername
    )
    
    if (hasMyReview) {
      alert('이미 이 영화에 리뷰를 작성하셨습니다.')
      return // 페이지 이동하지 않음
    }
  } catch (error) {
    // API 호출 실패 시에도 작성 페이지로 이동 (에러 무시)
    console.error('리뷰 확인 중 오류:', error)
  }
  
  // 리뷰가 없거나 현재 사용자가 작성한 리뷰가 없으면 작성 페이지로 이동
  // 백엔드 영화 API는 tmdb_id를 기대하므로 tmdb_id 전달
  router.push({ name: 'review-create', params: { id: movie.value.tmdb_id } })
}

const goBack = () => {
  router.push({ name: 'MovieDetail', params: { id: route.params.id } })
}

onMounted(() => {
  getMovieDetail()
})
</script>

<template>
  <div class="reviews-container" v-if="movie">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="goBack" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 헤더 -->
      <div class="reviews-header">
        <h3 class="reviews-title">{{ movie.title }}의 리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }}개)</h3>
        
        <div class="header-actions">
          <button v-if="store.isAuthenticated" @click="goCreateReview" class="btn-review-create">리뷰 작성하기</button>
        </div>
      </div>

      <!-- 정렬 선택 -->
      <div class="sort-section" v-if="movie.review_set && movie.review_set.length > 0">
        <select v-model="sortBy" class="sort-select">
          <option value="latest">최신순 (기본)</option>
          <option value="oldest">오래된 순</option>
          <option value="highRank">평점 높은 순</option>
          <option value="lowRank">평점 낮은 순</option>
          <option value="likes">좋아요 많은 순</option>
        </select>
      </div>

      <!-- 리뷰 목록 -->
      <div v-if="sortedReviews.length > 0" class="reviews-list">
        <div 
          v-for="review in sortedReviews" 
          :key="review.id" 
          @click="goDetail(review.id)" 
          class="review-card"
        >
          <div class="review-card-header">
            <div class="review-user-info">
              <div class="review-user-details">
                <div class="review-username">{{ review.user_nickname || review.user }}</div>
                <div class="review-date">
                  {{ new Date(review.created_at).toLocaleString() }}
                  <span v-if="isEdited(review.created_at, review.updated_at)" class="edited-badge">
                    (수정됨)
                  </span>
                </div>
              </div>
            </div>
            <div class="review-rating-badge">
              ★ {{ review.rank }}
            </div>
          </div>

          <div class="card-divider"></div>

          <div class="review-card-content">
            <h5 class="review-card-title">{{ review.title }}</h5>
            <p class="review-card-text">{{ review.content }}</p>
          </div>

          <div class="card-divider"></div>

          <div class="review-card-footer">
            <div class="review-stats">
              <span class="review-like-count">❤ {{ review.like_count || 0 }}</span>
              <span class="review-comment-count">💬 {{ review.comments ? review.comments.length : 0 }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-reviews">
        <p>아직 작성된 리뷰가 없습니다.</p>
        <p>첫 번째 리뷰의 주인공이 되어보세요!</p>
      </div>
    </div>
  </div>
  <div v-else class="loading-container">
    <div class="spinner-border text-light" role="status"></div>
  </div>
</template>

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

.header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-review-create {
  padding: 0.5rem 1.5rem;
  background-color: transparent;
  color: #999999;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-review-create:hover {
  color: #cccccc;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-review-create:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-review-create:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

/* 정렬 섹션 */
.sort-section {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.sort-select {
  padding: 0.5rem 1rem;
  background-color: #1a1a1a;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.sort-select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.3);
}

/* 리뷰 목록 */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 리뷰 카드 */
.review-card {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 22px;
  background-color: #1a1a1a;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.review-card:hover {
  background-color: #252525;
}

.review-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.review-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.review-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.review-username {
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
}

.review-date {
  font-size: 0.875rem;
  color: #999999;
}

.edited-badge {
  color: #999999;
  font-weight: 500;
  margin-left: 0.25rem;
}

.review-rating-badge {
  font-size: 1rem;
  color: #ffc107;
  font-weight: 500;
}

.card-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 1rem 0;
}

.review-card-content {
  margin-bottom: 0;
}

.review-card-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.75rem;
}

.review-card-text {
  font-size: 0.95rem;
  color: #cccccc;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0;
}

.review-card-footer {
  margin-top: 0;
}

.review-stats {
  display: flex;
  gap: 1rem;
  align-items: center;
  font-size: 0.9rem;
}

.review-like-count {
  color: #ffffff;
}

.review-comment-count {
  color: #999999;
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

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .btn-review-create {
    width: 100%;
  }
}
</style>
