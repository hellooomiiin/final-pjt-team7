<template>
  <div class="recommend-container">
    <div class="container">
      <div class="header-section">
        <h1>{{ moodMessage }}</h1>
        <p>이런 영화들이 기분 전환에 도움이 될 거예요!</p>
      </div>

      <div v-if="loading" class="loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else class="movies-grid">
        <div 
          v-for="movie in recommendedMovies" 
          :key="movie.tmdb_id" 
          class="movie-card"
          @click="goToDetail(movie.tmdb_id)"
        >
          <img 
            :src="getImageUrl(movie.poster_path)" 
            :alt="movie.title" 
          />
          <div class="movie-info">
            <h3>{{ movie.title }}</h3>
            <span class="rating">★ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</span>
          </div>
        </div>
      </div>
      
      <div class="action-area">
        <button @click="$router.push('/')" class="btn-back">다시 선택하기</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios' // [변경] axios 임포트

export default {
  name: 'RecommendView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const recommendedMovies = ref([])

    // URL 쿼리 파라미터에서 기분 가져오기 (?mood=xxx)
    const currentMood = computed(() => route.query.mood)

    // 기분에 따른 제목 표시
    const moodMessage = computed(() => {
      switch(currentMood.value) {
        case 'bored': return '🥱 심심할 땐, 시간 순삭 영화!';
        case 'angry': return '😡 화날 땐, 다 때려부수는 액션!';
        case 'sad': return '😢 슬플 땐, 실컷 울 수 있는 영화!';
        default: return '추천 영화 목록';
      }
    })

    // [중요] 백엔드 DB에서 데이터 가져오기
    const fetchRecommendations = async () => {
      loading.value = true
      try {
        // 1. 현재는 '인기 영화' API를 재사용합니다. 
        // (나중에 AI 기능이 완성되면 '/api/recommend/' 같은 전용 엔드포인트로 교체하면 됩니다)
        const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/popular/')
        
        // 2. 받아온 20개 영화 중 랜덤으로 섞어서 4개를 뽑습니다. (추천 느낌 내기)
        const allMovies = response.data
        const shuffled = allMovies.sort(() => 0.5 - Math.random())
        recommendedMovies.value = shuffled.slice(0, 4)
        
      } catch (err) {
        console.error('추천 영화 로드 실패:', err)
      } finally {
        loading.value = false
      }
    }

    // [추가] 이미지 URL 생성 함수
    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.jpg' // 없을 때 대체 이미지
      return `https://image.tmdb.org/t/p/w500${path}`
    }

    // [변경] tmdb_id 사용
    const goToDetail = (id) => {
      router.push(`/movies/${id}`)
    }

    onMounted(() => {
      if (!currentMood.value) {
        alert('잘못된 접근입니다.')
        router.push('/')
        return
      }
      fetchRecommendations()
    })

    return {
      moodMessage,
      recommendedMovies,
      loading,
      goToDetail,
      getImageUrl // 템플릿 반환
    }
  }
}
</script>

<style scoped>
/* 스타일은 기존 그대로 유지 */
.recommend-container { padding: 4rem 0; min-height: 80vh; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 1rem; }
.header-section { text-align: center; margin-bottom: 3rem; }
.header-section h1 { font-size: 2.5rem; margin-bottom: 1rem; font-weight: bold; }

.loading-spinner { text-align: center; padding: 3rem; }

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.movie-card {
  border: 1px solid #000;
  cursor: pointer;
  transition: transform 0.2s;
  background: white;
}
.movie-card:hover { transform: translateY(-5px); box-shadow: 5px 5px 0px #000; }
.movie-card img { width: 100%; height: 350px; object-fit: cover; border-bottom: 1px solid #000; }
.movie-info { padding: 1rem; text-align: center; }
.movie-info h3 { font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.action-area { text-align: center; }
.btn-back {
  padding: 0.8rem 2rem;
  background: black;
  color: white;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-back:hover { opacity: 0.8; }
</style>