<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const title = ref('')
const content = ref('')
const rank = ref(5) // ★ [추가] 평점 변수 (기본값 5)

// src/views/ReviewCreateView.vue

const createReview = async () => {
  // ... (유효성 검사 등은 그대로) ...

  console.log('현재 토큰 값:', store.token) 
  console.log('헤더 값:', `Token ${store.token}`)

  try {
    await axios({
      method: 'post',
      // ★ 1. 주소를 "전체 리뷰 주소"로 변경하세요.
      // (만약 /api/v1/reviews/ 가 아니면 팀원에게 '리뷰 작성 URL'을 물어봐야 합니다)
      url: `http://127.0.0.1:8000/api/v1/community/reviews/`, 
      headers: {
        Authorization: `Bearer ${store.token}`
      },
      data: {
        title: title.value,
        content: content.value,
        rank: rank.value,
        // ★ 2. "이 영화에 대한 리뷰입니다"라고 영화 ID를 같이 보내야 합니다.
        // 백엔드에서 영화 필드명이 'movie' 인지 'movie_id' 인지 확인 필요 (보통 'movie')
        movie: route.params.id 
      }
    })
    
    alert('리뷰가 등록되었습니다!')
    router.push({ name: 'movie-reviews', params: { id: route.params.id } })
    
  } catch (err) {
    console.log('에러 응답:', err.response?.data)
    alert('작성 실패! 콘솔(F12)을 확인해주세요.')
  }
}
</script>

<template>
  <div class="container mt-5">
    <h2>리뷰 작성</h2>
    <hr>
    
    <div class="mb-3">
      <label class="form-label">제목</label>
      <input v-model="title" type="text" class="form-control">
    </div>

    <div class="mb-3">
      <label class="form-label">평점 (1~10)</label>
      <input v-model="rank" type="number" min="1" max="10" class="form-control">
    </div>

    <div class="mb-3">
      <label class="form-label">내용</label>
      <textarea v-model="content" class="form-control" rows="5"></textarea>
    </div>

    <div class="d-flex gap-2">
      <button @click="createReview" class="btn btn-primary">등록완료</button>
      <button @click="router.go(-1)" class="btn btn-secondary">취소</button>
    </div>
  </div>
</template>