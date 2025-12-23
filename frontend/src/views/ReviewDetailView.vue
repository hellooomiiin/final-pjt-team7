<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const review = ref(null)
const commentContent = ref('') // 댓글 입력 데이터

const isEdited = (created, updated) => {
  const createdTime = new Date(created).getTime()
  const updatedTime = new Date(updated).getTime()
  return updatedTime - createdTime > 2000
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

// 5. 리뷰 자체 삭제
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

onMounted(() => {
  getReviewDetail()
})
</script>

<template>
  <div class="container mt-5" v-if="review">
    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center bg-light">
        <span class="fw-bold">{{ review.user_nickname || review.user }}님의 리뷰</span>
        <span class="text-muted small">
          {{ new Date(review.created_at).toLocaleString() }}
          <span v-if="isEdited(review.created_at, review.updated_at)" class="ms-1 fw-bold">
            (수정됨)
          </span>
        </span>
      </div>
      <div class="card-body">
        <h2 class="card-title mb-3">{{ review.title }}</h2>
        <h4 class="text-warning mb-4">★ {{ review.rank }}</h4>
        <p class="card-text fs-5 mb-5">{{ review.content }}</p>

        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center gap-2">
            <button 
              v-if="store.isAuthenticated"
              @click="toggleLike" 
              :class="['btn', 'd-flex', 'align-items-center', 'gap-2', isLiked ? 'btn-like-active' : 'btn-like-inactive']"
            >
              <span v-if="isLiked">♥</span>
              <span v-else>♡</span>
              <span>좋아요 {{ review.like_count }}</span>
            </button>
            <span v-else class="text-muted">좋아요 {{ review.like_count }}</span>
          </div>

          <div v-if="review.user === store.user?.username" class="d-flex gap-2">
            <button @click="$router.push({name: 'review-update'})" class="btn btn-sm btn-outline-primary">수정</button>
            <button @click="deleteReview" class="btn btn-sm btn-outline-danger">삭제</button>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-5">
      <h4>댓글 ({{ review.comments ? review.comments.length : 0 }})</h4>
      <hr>

      <form v-if="store.isAuthenticated" @submit.prevent="createComment" class="input-group mb-4">
        <input 
          type="text" 
          class="form-control" 
          v-model="commentContent" 
          placeholder="댓글을 남겨주세요..." 
          required
        >
        <button class="btn btn-primary" type="submit">등록</button>
      </form>
      <div v-else class="mb-4 p-3 bg-light rounded text-center text-muted">
        댓글을 작성하려면 <router-link to="/login">로그인</router-link>이 필요합니다.
      </div>

      <div v-if="review.comments && review.comments.length > 0">
        <ul class="list-group list-group-flush">
          <li 
            v-for="comment in review.comments" 
            :key="comment.id" 
            class="list-group-item d-flex justify-content-between align-items-start bg-transparent"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold mb-1">{{ comment.user_nickname || comment.user }}</div>
              {{ comment.content }}
            </div>
            
            <div v-if="comment.user === store.user?.username">
              <button @click="deleteComment(comment.id)" class="btn btn-sm btn-link text-danger text-decoration-none">x</button>
            </div>
          </li>
        </ul>
      </div>
      <div v-else class="text-center py-4 text-muted">
        첫 번째 댓글을 남겨보세요!
      </div>
    </div>

    <div class="mt-4 text-center">
      <button @click="router.push({ name: 'movie-reviews', params: { id: route.params.id } })" class="btn btn-secondary">뒤로가기</button>
    </div>
  </div>

  <div v-else class="text-center mt-5">
    <div class="spinner-border text-primary" role="status"></div>
  </div>
</template>

<style scoped>
.btn-like-active {
  background-color: #f7429c;
  border-color: #ee5fa7;
  color: white;
}

.btn-like-active:hover {
  background-color: #fd3fa5;
  border-color: #f849a6;
  color: white;
}

.btn-like-inactive {
  background-color: transparent;
  border-color: #f84da3;
  color: #000000;
}

.btn-like-inactive:hover {
  background-color: #f03d96;
  border-color: #f877b8;
  color: white;
}
</style>