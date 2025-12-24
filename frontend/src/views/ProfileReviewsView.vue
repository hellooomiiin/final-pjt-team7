<template>
  <div class="profile-reviews-container">
    <div class="container">
      <div class="mb-4 d-flex justify-content-between align-items-center">
        <button @click="$router.push('/profile')" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
        <h2 class="mb-0 fw-bold">내 작성 리뷰</h2>
      </div>

      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩 중...</span>
        </div>
        <p class="mt-2 text-muted">리뷰를 불러오고 있습니다.</p>
      </div>

      <div v-else-if="myReviews && myReviews.length > 0">
        <div v-for="review in myReviews" :key="review.id" class="card mb-4 shadow-sm border-0 overflow-hidden review-card">
          <div class="row g-0">
            <div class="col-3 col-md-2">
              <img 
                :src="review.movie_poster ? `https://image.tmdb.org/t/p/w200${review.movie_poster}` : '/assets/no-poster.png'" 
                class="img-fluid h-100 poster-img" 
                alt="movie poster"
                style="object-fit: cover; min-height: 160px;"
              >
            </div>
            
            <div class="col-9 col-md-10">
              <div class="card-body p-3 p-md-4 d-flex flex-column h-100">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <p class="movie-title-label text-primary fw-bold mb-1">
                      {{ review.movie_title }}
                    </p>
                    <h5 class="card-title fw-bold mb-0 text-truncate">
                      {{ review.title }}
                    </h5>
                  </div>
                    <StarDisplay :rating="review.rank" />
                </div>
                
                <p class="card-text text-muted mb-3 flex-grow-1 text-break review-content-preview">
                  {{ review.content }}
                </p>
                
                <div class="d-flex justify-content-between align-items-center mt-auto pt-2 border-top">
                  <div class="d-flex gap-3 text-secondary small">
                    <span>❤️ {{ review.like_count || 0 }}</span>
                    <span>💬 {{ review.comments ? review.comments.length : 0 }}</span>
                    <span class="d-none d-sm-inline">| {{ new Date(review.created_at).toLocaleDateString() }}</span>
                  </div>
                  <router-link 
                    :to="{ name: 'review-detail', params: { id: review.movie, reviewId: review.id } }" 
                    class="btn btn-sm btn-dark px-3"
                  >
                    상세보기
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state text-center py-5 border rounded bg-light">
        <p class="text-muted mb-0">아직 작성한 리뷰가 없습니다. 영화에 대한 첫 리뷰를 남겨보세요!</p>
      </div>
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
.profile-reviews-container {
  min-height: calc(100vh - 80px);
  padding: 2rem 0;
  background-color: #f8f9fa;
}

.review-card {
  transition: transform 0.2s ease-in-out;
  border-radius: 12px;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.movie-title-label {
  font-size: 0.85rem;
}

.review-content-preview {
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 2줄까지만 보여주고 말줄임표 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.95rem;
}

.poster-img {
  transition: opacity 0.3s;
}

.card:hover .poster-img {
  opacity: 0.9;
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
</style>