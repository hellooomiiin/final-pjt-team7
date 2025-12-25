<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const review = ref(null)
const movie = ref(null)
const commentContent = ref('') // 댓글 입력 데이터

const isEdited = (created, updated) => {
  const createdTime = new Date(created).getTime()
  const updatedTime = new Date(updated).getTime()
  return updatedTime - createdTime > 2000
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '오늘'
  if (diffDays === 1) return '어제'
  if (diffDays < 7) return `${diffDays}일 전`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}주 전`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}개월 전`
  return `${Math.floor(diffDays / 365)}년 전`
}

const getImageUrl = (path, type = 'poster') => {
  if (!path) return type === 'poster' ? '/assets/no-poster.png' : '/assets/no-profile.png'
  const size = type === 'poster' ? 'w500' : 'w185'
  return `https://image.tmdb.org/t/p/${size}${path}`
}

// 1. 리뷰 상세 정보 (+댓글) 가져오기 (토큰 없이도 조회 가능)
const getReviewDetail = async () => {
  try {
    const res = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/`
    })
    review.value = res.data
    console.log('리뷰 정보:', res.data)
    
    // 영화 정보 가져오기
    if (res.data.movie_tmdb_id) {
      try {
        const movieRes = await axios({
          method: 'get',
          url: `http://127.0.0.1:8000/api/v1/movies/${res.data.movie_tmdb_id}/`
        })
        movie.value = movieRes.data
      } catch (err) {
        console.error('영화 정보 로드 실패:', err)
      }
    }
  } catch (err) {
    console.error(err)
  }
}

// 2. 좋아요 기능
const toggleLike = async () => {
  try {
    const res = await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/likes/`,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    
    // 백엔드에서 보낸 'liked'(좋아요 여부)와 'count'(개수)로 화면 갱신
    if (review.value) {
      review.value.like_count = res.data.count
      
      // 내 아이디가 리스트에 있는지 확인해서 is_liked 갱신 (간단한 처리)
      if (res.data.liked) {
        // 좋아요 눌렀으면 내 아이디 추가 (화면 갱신용)
        if (!review.value.like_users) {
          review.value.like_users = []
        }
        review.value.like_users.push(store.user.id) 
      } else {
        // 취소했으면 내 아이디 제거
        review.value.like_users = review.value.like_users.filter(id => id !== store.user.id)
      }
    }
  } catch (err) {
    console.error(err)
    alert('좋아요 실패!')
  }
}

// 3. 댓글 작성 (Create)
const createComment = async () => {
  if (!commentContent.value.trim()) {
    alert('댓글 내용을 입력해주세요!')
    return
  }

  try {
    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/comments/`,
      headers: { Authorization: `Bearer ${store.token}` },
      data: { content: commentContent.value }
    })
    
    commentContent.value = '' // 입력창 비우기
    getReviewDetail()         // 댓글 목록 다시 불러오기 (새로고침)
    
  } catch (err) {
    console.error(err)
    alert('댓글 작성 실패...')
  }
}

// 4. 댓글 삭제 (Delete)
const deleteComment = async (commentId) => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  try {
    await axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/comments/${commentId}/`,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    getReviewDetail() // 목록 갱신
  } catch (err) {
    console.error(err)
    alert('삭제 실패! 권한이 없습니다.')
  }
}

// 5. 뒤로가기
const goBack = () => {
  // 프로필에서 온 경우 프로필 리뷰 목록으로
  if (route.query.from === 'profile') {
    router.push('/profile/reviews')
  } else {
    // 영화 상세에서 온 경우: movie.tmdb_id를 사용
    if (movie.value && movie.value.tmdb_id) {
      router.push({ name: 'movie-reviews', params: { id: movie.value.tmdb_id } })
    } else if (review.value && review.value.movie_tmdb_id) {
      // movie 정보가 아직 로드되지 않았을 경우 review에서 가져온 tmdb_id 사용
      router.push({ name: 'movie-reviews', params: { id: review.value.movie_tmdb_id } })
    } else {
      // fallback: route.params.id 사용 (tmdb_id일 것으로 예상)
      router.push({ name: 'movie-reviews', params: { id: route.params.id } })
    }
  }
}

// 6. 리뷰 수정 페이지로 이동
const goToUpdate = () => {
  router.push({ name: 'review-update', params: { id: route.params.id, reviewId: route.params.reviewId } })
}

// 7. 리뷰 자체 삭제
const deleteReview = async () => {
  if (!confirm('정말 리뷰를 삭제하시겠습니까?')) return
  try {
    await axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/`,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    alert('리뷰가 삭제되었습니다.')
    router.push({ name: 'movie-reviews', params: { id: route.params.id } })
  } catch (err) {
    console.error(err)
  }
}

// 현재 좋아요 상태 확인 (computed)
const isLiked = computed(() => {
  // like_users 배열에 내 ID가 있으면 true
  return review.value?.like_users?.includes(store.user?.id)
})

const getYear = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).getFullYear()
}

onMounted(() => {
  getReviewDetail()
})
</script>

<template>
  <div class="review-detail-container" v-if="review">
    <div class="review-post">
      <!-- 뒤로가기 버튼 -->
      <button @click="goBack" class="back-button">
        ← 뒤로가기
      </button>

      <!-- 리뷰 카드 (글쓴이부터 좋아요 수까지) -->
      <div class="review-main-card">
        <!-- 사용자 정보 헤더 -->
        <div class="review-header">
          <div class="user-info">
            <div class="user-details">
              <div class="username">{{ review.user_nickname || review.user }}</div>
              <div class="post-date">
                {{ new Date(review.created_at).toLocaleString() }}
                <span v-if="isEdited(review.created_at, review.updated_at)" class="edited-badge">
                  (수정됨)
                </span>
              </div>
            </div>
          </div>
          <div class="rating-badge">
            ★ {{ review.rank }}
          </div>
        </div>

        <!-- 구분선 -->
        <div class="card-divider"></div>

        <!-- 영화 정보 -->
        <div class="movie-info-section" v-if="movie || review.movie_title">
          <div class="movie-poster">
            <img 
              :src="getImageUrl(movie?.poster_path || review.movie_poster, 'poster')" 
              :alt="movie?.title || review.movie_title"
            />
          </div>
          <div class="movie-info">
            <div class="movie-title-row">
              <span class="movie-title">{{ movie?.title || review.movie_title }}</span>
            </div>
            <div class="movie-meta">
              <span>영화</span>
            </div>
          </div>
        </div>

        <!-- 구분선 -->
        <div v-if="movie || review.movie_title" class="card-divider"></div>

        <!-- 리뷰 내용 -->
        <div class="review-content">
          <div class="review-title-section">
            <h2 class="review-title">{{ review.title }}</h2>
            <div v-if="review.user === store.user?.username" class="review-actions-buttons">
              <button @click="goToUpdate" class="review-edit-btn">수정</button>
              <button @click="deleteReview" class="review-delete-btn">삭제</button>
            </div>
          </div>
          <p class="review-text">{{ review.content }}</p>
        </div>

        <!-- 구분선 -->
        <div class="card-divider"></div>

        <!-- 좋아요 버튼 -->
        <div class="review-like-section">
          <button 
            v-if="store.isAuthenticated"
            @click="toggleLike" 
            class="like-btn"
            :class="{ 'liked': isLiked }"
          >
            <span class="like-icon">❤</span>
            <span class="like-count-text">{{ review.like_count || 0 }}</span>
          </button>
          <div v-else class="like-btn-disabled">
            <span class="like-icon">❤</span>
            <span class="like-count-text">{{ review.like_count || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="divider"></div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h4 class="comments-title">댓글 ({{ review.comments ? review.comments.length : 0 }})</h4>

        <form v-if="store.isAuthenticated" @submit.prevent="createComment" class="comment-form">
          <input 
            type="text" 
            class="comment-input" 
            v-model="commentContent" 
            placeholder="댓글을 남겨주세요..." 
            required
          >
          <button class="comment-submit" type="submit">등록</button>
        </form>
        <div v-else class="comment-login-prompt">
          댓글을 작성하려면 <router-link to="/login">로그인</router-link>이 필요합니다.
        </div>

        <div v-if="review.comments && review.comments.length > 0" class="comments-list">
          <div 
            v-for="comment in review.comments" 
            :key="comment.id" 
            class="comment-item"
          >
            <div class="comment-header">
              <div class="comment-user-info">
                <div class="comment-user-details">
                  <div class="comment-username">{{ comment.user_nickname || comment.user }}</div>
                  <div class="comment-date">
                    {{ new Date(comment.created_at).toLocaleString() }}
                    <span v-if="isEdited(comment.created_at, comment.updated_at)" class="edited-badge">
                      (수정됨)
                    </span>
                  </div>
                </div>
              </div>
              <button 
                v-if="comment.user === store.user?.username"
                @click="deleteComment(comment.id)" 
                class="comment-delete-btn"
              >
                삭제
              </button>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
          </div>
        </div>
        <div v-else class="no-comments">
          첫 번째 댓글을 남겨보세요!
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading-container">
    <div class="spinner-border text-light" role="status"></div>
  </div>
</template>

<style scoped>
.review-detail-container {
  min-height: calc(100vh - 80px);
  background-color: #000000;
  color: #ffffff;
  padding: 2rem 0;
}

.review-post {
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

/* 리뷰 메인 카드 */
.review-main-card {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 22px;
  background-color: #1a1a1a;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

/* 사용자 정보 헤더 */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.card-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 1rem 0;
}

.review-content + .card-divider {
  margin: 0.5rem 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.username {
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
}

.post-date {
  font-size: 0.875rem;
  color: #999999;
}

.edited-badge {
  color: #999999;
  font-weight: 500;
  margin-left: 0.25rem;
}

.rating-badge {
  font-size: 1rem;
  color: #ffc107;
  font-weight: 500;
}

/* 영화 정보 섹션 (카드 내부) */
.movie-info-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 0;
}

.movie-poster {
  width: 80px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
}

.movie-title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.movie-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
}

.movie-release-date {
  font-size: 1.1rem;
  color: #999999;
}

.movie-rating-inline {
  font-size: 1.1rem;
  color: #cccccc;
}

.movie-meta {
  font-size: 0.875rem;
  color: #999999;
}

.movie-review-info {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.review-title-small {
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.review-like-count-small {
  font-size: 0.875rem;
  color: #ffffff;
}

/* 리뷰 내용 */
.review-content {
  margin-bottom: 0;
}

.review-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.review-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0;
}

.review-actions-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.review-edit-btn,
.review-delete-btn {
  background: none;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  color: #999999;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  transition: color 0.2s;
}

.review-edit-btn:hover,
.review-delete-btn:hover {
  color: #ffffff;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.review-edit-btn:focus,
.review-delete-btn:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.review-edit-btn:active,
.review-delete-btn:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.review-text {
  font-size: 1rem;
  color: #cccccc;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* 좋아요 버튼 */
.review-like-section {
  margin-bottom: 0;
}

.like-btn {
  background: none;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  color: #ffffff;
  font-size: 1rem;
  cursor: pointer;
  padding: 4px 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.like-btn:hover {
  opacity: 0.8;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.like-btn:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.like-btn:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.like-btn.liked {
  color: #ff6b6b;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.like-btn-disabled {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ffffff;
  font-size: 1rem;
  padding: 4px 0;
  opacity: 0.7;
}

.like-icon {
  font-size: 1.2rem;
}

.like-count-text {
  font-size: 0.9rem;
}

/* 구분선 */
.divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 1.5rem 0;
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 2rem;
}

.comments-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 1.5rem;
}

.comment-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.comment-input {
  flex: 1;
  padding: 0.75rem;
  background-color: #1a1a1a;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.9rem;
}

.comment-input:focus {
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
}

.comment-input:active {
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
}

.comment-submit {
  padding: 0.75rem 1.5rem;
  background-color: #666666;
  color: #ffffff;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.comment-submit:hover {
  background-color: #777777;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-submit:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-submit:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-login-prompt {
  padding: 1rem;
  background-color: #1a1a1a;
  border-radius: 4px;
  text-align: center;
  color: #999999;
  margin-bottom: 2rem;
}

.comment-login-prompt a {
  color: #ffffff;
  text-decoration: underline;
}

/* 댓글 목록 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-item {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.comment-user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.comment-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.comment-username {
  font-size: 0.9rem;
  font-weight: 500;
  color: #ffffff;
}

.comment-date {
  font-size: 0.8rem;
  color: #999999;
}

.comment-date .edited-badge {
  color: #999999;
  font-weight: 500;
  margin-left: 0.25rem;
}

.comment-delete-btn {
  background: none;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  color: #999999;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  transition: color 0.2s;
}

.comment-delete-btn:hover {
  color: #ffffff;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-delete-btn:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-delete-btn:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.comment-content {
  font-size: 0.9rem;
  color: #cccccc;
  line-height: 1.6;
  white-space: pre-wrap;
}

.no-comments {
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
  .review-post {
    padding: 0 0.5rem;
  }

  .movie-card {
    flex-direction: column;
  }

  .movie-poster {
    width: 100%;
    height: auto;
    aspect-ratio: 2 / 3;
  }
}
</style>
