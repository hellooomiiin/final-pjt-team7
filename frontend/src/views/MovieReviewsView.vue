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

onMounted(() => {
  getMovieDetail()
})
</script>

<template>
  <div class="container mt-5" v-if="movie">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>{{ movie.title }}의 리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }}개)</h3>
      
      <div class="d-flex gap-2">
        <button v-if="store.isAuthenticated" @click="goCreateReview" class="btn btn-primary">리뷰 작성하기</button>
        <button @click="router.push({ name: 'MovieDetail', params: { id: route.params.id } })" class="btn btn-secondary">뒤로가기</button>
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
            작성자: {{ review.user_nickname || review.user }}
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