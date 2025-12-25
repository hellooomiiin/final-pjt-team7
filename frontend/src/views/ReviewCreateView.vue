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

const goBack = () => {
  // route.params.id는 tmdb_id이므로 리뷰 목록 페이지로 이동
  router.push({ name: 'movie-reviews', params: { id: route.params.id } })
}
</script>

<template>
  <div class="reviews-container">
    <div class="reviews-wrapper">
      <!-- 뒤로가기 버튼 -->
      <button @click="goBack" class="back-button">
        ← 뒤로가기
      </button>

      <div class="edit-card">
        <h2 class="edit-title">리뷰 작성</h2>
        
        <form @submit.prevent="createReview">
          <div class="form-group">
            <label class="form-label">제목</label>
            <input v-model="title" type="text" class="form-control" required>
          </div>

          <div class="form-group">
            <label class="form-label fw-bold">평점</label>
            <StarInput v-model="rank" />
          </div>

          <div class="form-group">
            <label class="form-label">내용</label>
            <textarea v-model="content" class="form-control" rows="5" required></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-submit">등록완료</button>
            <button type="button" @click="goBack" class="btn-cancel">취소</button>
          </div>
        </form>
      </div>
    </div>
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

.edit-card {
  background-color: #1a1a1a;
  padding: 22px;
  border-radius: 8px;
}

.edit-title {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  color: #ffffff;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  background-color: #333333;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border-radius: 4px;
  font-size: 1rem;
}

.form-control:focus {
  background-color: #333333;
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1);
}

.form-control::placeholder {
  color: #666666;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-submit,
.btn-cancel {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit {
  background-color: #1a1a1a;
  color: #ffffff;
}

.btn-submit:hover {
  background-color: #252525;
}

.btn-cancel {
  background-color: #333333;
  color: #ffffff;
}

.btn-cancel:hover {
  background-color: #444444;
}

@media (max-width: 768px) {
  .reviews-wrapper {
    padding: 0 0.5rem;
  }

  .edit-card {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
