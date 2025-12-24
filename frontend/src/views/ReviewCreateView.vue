<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import StarInput from '@/components/StarInput.vue'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const title = ref('')
const content = ref('')
const rank = ref(5) // ★ [추가] 평점 변수 (기본값 5)

// src/views/ReviewCreateView.vue

const createReview = async () => {
  try {
    // route.params.id가 tmdb_id일 수도 있고 DB의 id일 수도 있음
    // 영화 정보를 가져와서 DB의 id와 tmdb_id를 모두 얻기
    const movieRes = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`
    })
    const movieDbId = movieRes.data.id // DB의 id
    const tmdbId = movieRes.data.tmdb_id // tmdb_id (리다이렉트용)
    
    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/community/reviews/`, 
      headers: {
        Authorization: `Bearer ${store.token}`
      },
      data: {
        title: title.value,
        content: content.value,
        rank: rank.value,
        // DB의 id 사용
        movie: movieDbId
      }
    })
    
    alert('리뷰가 등록되었습니다!')
    // movie-reviews로 이동할 때는 tmdb_id 사용
    router.push({ name: 'movie-reviews', params: { id: tmdbId } })
    
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
    
    <form @submit.prevent="createReview">
      <div class="mb-3">
        <label class="form-label">제목</label>
        <input v-model="title" type="text" class="form-control" required>
      </div>

      <div class="mb-3">
        <label class="fw-bold">평점</label>
        <StarInput v-model="rank" />
      </div>

      <div class="mb-3">
        <label class="form-label">내용</label>
        <textarea v-model="content" class="form-control" rows="5" required></textarea>
      </div>

      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">등록완료</button>
        <button type="button" @click="router.go(-1)" class="btn btn-secondary">취소</button>
      </div>
    </form>
  </div>
</template>