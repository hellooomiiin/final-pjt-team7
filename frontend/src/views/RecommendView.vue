<template>
  <div class="recommend-container">
    <div class="container">
      <div class="header-section">
        <h1>{{ moodMessage }}</h1>
        <p>이런 영화들이 기분 전환에 도움이 될 거예요!</p>
      </div>

      <div v-if="loading" class="loading-spinner">
        Loading...
      </div>

      <div v-else class="movies-grid">
        <div 
          v-for="movie in recommendedMovies" 
          :key="movie.id" 
          class="movie-card"
          @click="goToDetail(movie.id)"
        >
          <img :src="movie.poster_path || '/placeholder.jpg'" :alt="movie.title" />
          <div class="movie-info">
            <h3>{{ movie.title }}</h3>
            <span class="rating">★ {{ movie.vote_average }}</span>
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
import { mockApi } from '@/data/mockData' 

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

    // 실제로는 백엔드에 mood를 보내서 데이터를 받아와야 함
    // 여기서는 mockApi의 데이터를 가져온 뒤 섞는 것으로 흉내만
    const fetchRecommendations = async () => {
      loading.value = true
      try {
        // 백엔드 API가 있다면: await axios.get(`/api/recommend?mood=${currentMood.value}`)
        const res = await mockApi.getPopularMovies() 
        // 예시를 위해 데이터를 조금 섞거나 잘라서 보여줍니다.
        recommendedMovies.value = res.data.slice(0, 4) 
      } catch (err) {
        console.error(err)
      } finally {
        loading.value = false
      }
    }

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
      goToDetail
    }
  }
}
</script>

<style scoped>
.recommend-container { padding: 4rem 0; min-height: 80vh; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 1rem; }
.header-section { text-align: center; margin-bottom: 3rem; }
.header-section h1 { font-size: 2.5rem; margin-bottom: 1rem; font-weight: bold; }

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
}
.movie-card:hover { transform: translateY(-5px); }
.movie-card img { width: 100%; height: 350px; object-fit: cover; }
.movie-info { padding: 1rem; text-align: center; }
.movie-info h3 { font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: bold; }

.action-area { text-align: center; }
.btn-back {
  padding: 0.8rem 2rem;
  background: black;
  color: white;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}
</style>