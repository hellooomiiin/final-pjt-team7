<template>
  <div class="reviews-container" v-if="!isLoading">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="$router.push('/profile')" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 헤더 -->
      <div class="reviews-header">
        <h3 class="reviews-title">내 작성 리뷰</h3>
      </div>

      <!-- 리뷰 목록 -->
      <div v-if="myReviews && myReviews.length > 0" class="reviews-list">
        <div 
          v-for="review in myReviews" 
          :key="review.id" 
          @click="$router.push({ name: 'review-detail', params: { id: review.movie, reviewId: review.id }, query: { from: 'profile' } })"
          class="review-card"
        >
          <div class="review-card-header">
            <div class="review-user-info">
              <div class="review-user-avatar">
                <div class="avatar-placeholder"></div>
              </div>
              <div class="review-user-details">
                <div class="review-username">{{ review.user_nickname || review.user }}</div>
                <div class="review-date">
                  {{ new Date(review.created_at).toLocaleString() }}
                </div>
              </div>
            </div>
            <div class="review-rating-badge">
              ★ {{ review.rank }}
            </div>
          </div>

          <div class="card-divider"></div>

          <div class="review-card-content">
            <div class="movie-title-label">{{ review.movie_title }}</div>
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
        <p>아직 작성한 리뷰가 없습니다.</p>
        <p>영화에 대한 첫 리뷰를 남겨보세요!</p>
      </div>
    </div>
  </div>
  <div v-else class="loading-container">
    <div class="spinner-border text-light" role="status">
      <span class="visually-hidden">로딩 중...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import StarDisplay from '@/components/StarDisplay.vue'

// 컴포넌트 이름 정의 (script setup에서는 필수는 아니지만 명시할 때 사용)
defineOptions({
  name: 'ProfileReviewsView'
})

const store = useAuthStore()
const myReviews = ref([])
const isLoading = ref(true)

const fetchMyReviews = async () => {
  isLoading.value = true
  try {
    const res = await axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/community/my-reviews/',
      headers: {
        Authorization: `Bearer ${store.token}`
      }
    })
    myReviews.value = res.data
  } catch (err) {
    console.error('내 리뷰 로드 실패:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchMyReviews()
})
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

.review-user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: #333333;
  border-radius: 50%;
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

.movie-title-label {
  font-size: 0.85rem;
  color: #999999;
  margin-bottom: 0.5rem;
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
}
</style>
