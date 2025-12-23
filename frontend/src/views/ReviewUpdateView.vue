<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const title = ref('')
const content = ref('')
const rank = ref(5) // 기본값 5점

// 1. 기존 리뷰 데이터 가져오기
const getReview = async () => {
  try {
    const res = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/`,
      headers: { Authorization: `Bearer ${store.token}` }
    })
    // 가져온 데이터로 빈칸 채우기
    title.value = res.data.title
    content.value = res.data.content
    rank.value = res.data.rank
  } catch (err) {
    console.error(err)
  }
}

// 2. 수정 요청 보내기 (PUT)
const updateReview = async () => {
  try {
    await axios({
      method: 'put', // ★ 수정은 put!
      url: `http://127.0.0.1:8000/api/v1/community/reviews/${route.params.reviewId}/`,
      headers: { Authorization: `Bearer ${store.token}` },
      data: {
        title: title.value,
        content: content.value,
        rank: rank.value,
        movie: Number(route.params.id) // 영화 ID 필수
      }
    })
    
    alert('수정 완료!')
    // 수정 후 상세 페이지로 이동
    router.push({ 
      name: 'review-detail', 
      params: { id: route.params.id, reviewId: route.params.reviewId } 
    })
    
  } catch (err) {
    console.error(err)
    alert('수정 실패...')
  }
}

onMounted(() => {
  getReview()
})
</script>

<template>
  <div class="container mt-5">
    <h2>리뷰 수정</h2>
    <hr>
    
    <form @submit.prevent="updateReview">
      <div class="mb-3">
        <label class="form-label">제목</label>
        <input v-model="title" type="text" class="form-control" required>
      </div>

      <div class="mb-3">
        <label class="form-label">평점</label>
        <div class="d-flex gap-3 align-items-center">
          <label v-for="rating in [1, 2, 3, 4, 5]" :key="rating" class="d-flex align-items-center gap-2">
            <input 
              type="radio" 
              :value="rating" 
              v-model="rank"
              class="form-check-input"
              required
            >
            <span>{{ rating }}점</span>
          </label>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">내용</label>
        <textarea v-model="content" class="form-control" rows="5" required></textarea>
      </div>

      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">수정완료</button>
        <button type="button" @click="router.go(-1)" class="btn btn-secondary">취소</button>
      </div>
    </form>
  </div>
</template>