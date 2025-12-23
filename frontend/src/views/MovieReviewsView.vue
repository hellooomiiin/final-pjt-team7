<script setup>
import { ref, onMounted, computed } from 'vue' // ★ computed 추가
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

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
    const res = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    movie.value = res.data
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

const goCreateReview = () => {
  router.push({ name: 'review-create', params: { id: route.params.id } })
}

onMounted(() => {
  getMovieDetail()
})
</script>

<template>
  <div class="container mt-5" v-if="movie">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>{{ movie.title }}의 리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }}개)</h3>
      
      <div class="d-flex gap-2">
        <button @click="goCreateReview" class="btn btn-primary">리뷰 작성하기</button>
        <button @click="router.go(-1)" class="btn btn-secondary">뒤로가기</button>
      </div>
    </div>
    <hr>

    <div class="d-flex justify-content-end mb-3" v-if="movie.review_set && movie.review_set.length > 0">
      <select v-model="sortBy" class="form-select w-auto">
        <option value="latest">최신순 (기본)</option>
        <option value="oldest">오래된 순</option>
        <option value="highRank">평점 높은 순</option>
        <option value="lowRank">평점 낮은 순</option>
        <option value="likes">좋아요 많은 순</option>
      </select>
    </div>

    <div v-if="sortedReviews.length > 0">
      <div 
        v-for="review in sortedReviews" 
        :key="review.id" 
        @click="goDetail(review.id)" 
        class="card mb-3 hover-effect"
        style="cursor: pointer;"
      >
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h5 class="card-title text-truncate mb-0" style="max-width: 80%;">
              {{ review.title }} 
            </h5>
            <span class="badge bg-warning text-dark">★ {{ review.rank }}</span>
          </div>
          
          <h6 class="card-subtitle my-2 text-muted small">
            작성자: {{ review.user }}
          </h6>
          
          <p class="card-text text-truncate">{{ review.content }}</p>
          
          <div class="d-flex justify-content-between align-items-center mt-3 border-top pt-2">
            <small class="text-muted">
              {{ new Date(review.created_at).toLocaleString() }}
              <span v-if="isEdited(review.created_at, review.updated_at)" class="ms-1 text-secondary fw-bold">
                (수정됨)
              </span>
            </small>
            
            <div class="d-flex gap-3 text-secondary small">
              <span class="d-flex align-items-center gap-1">
                ❤ {{ review.like_count || 0 }}
              </span>
              <span class="d-flex align-items-center gap-1">
                💬 {{ review.comments ? review.comments.length : 0 }}
              </span>
          </div>
        </div>

        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <p class="text-muted">아직 작성된 리뷰가 없습니다.</p>
      <p>첫 번째 리뷰의 주인공이 되어보세요!</p>
    </div>

  </div>
  <div v-else class="text-center mt-5">
    <p>로딩중...</p>
  </div>
</template>

<style scoped>
.hover-effect:hover {
  background-color: #f8f9fa;
  transition: 0.3s;
}
</style>