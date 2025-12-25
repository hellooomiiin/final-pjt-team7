<template>
  <div class="home-container">
    <div v-if="showMoodModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">오늘의 기분은 어떠신가요?</h3>
        <p class="modal-subtitle">기분에 딱 맞는 영화를 추천해 드릴게요.</p>
        
        <div class="mood-buttons">
          <button 
            v-for="mood in moodOptions" 
            :key="mood.key"
            @click="selectMood(mood.key)" 
            class="btn-mood"
          >
            <span class="emoji">{{ mood.emoji }}</span> {{ mood.label }}
          </button>
        </div>
        
        <button class="btn-close-modal" @click="closeModal">닫기</button>
      </div>
    </div>

    <div class="container">
			<div class="search-section text-center mb-5">
        <form @submit.prevent="onSearch" class="search-form">
          <input 
            type="text" 
            v-model="keyword" 
            class="form-control search-input" 
            placeholder="영화 제목을 검색해보세요 (예: 해리포터)"
          >
          <button type="submit" class="btn btn-dark search-btn">검색</button>
        </form>
      </div>
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">
            <span class="check-icon">✓</span>
            Mood-Match에 오신 것을 환영합니다
          </h1>
          <p class="welcome-subtitle">
            AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다
          </p>
          <button v-if="!showMoodModal" @click="showMoodModal = true" class="btn btn-outline-dark btn-sm mt-2">
            ✨ 기분 다시 선택하기
          </button>
        </div>
      </div>

      <div class="popular-movies-section">
        <h2 class="section-title">인기 영화</h2>
        <p class="section-subtitle">지금 가장 많이 찾는 영화들을 만나보세요</p>
        
        <div v-if="loading" class="text-center loading-spinner">
          <div class="spinner-border text-danger" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else class="movies-scroll-container">
          <div class="movies-grid">
            <div
              v-for="movie in popularMovies"
              :key="movie.tmdb_id"
              class="movie-card-item"
              @click="goToMovieDetail(movie.tmdb_id)"
            >
              <div class="movie-card">
                <img
                  :src="getImageUrl(movie.poster_path)"
                  class="movie-poster"
                  :alt="movie.title"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const popularMovies = ref([])
    const loading = ref(true)
    const showMoodModal = ref(false)

    // [수정] 백엔드 매핑과 일치하는 5가지 감정 옵션 정의
    const moodOptions = [
      { key: 'bored', label: '심심해요', emoji: '🥱' },
      { key: 'angry', label: '화나요', emoji: '😡' },
      { key: 'sad', label: '슬퍼요', emoji: '😢' },
      { key: 'happy', label: '행복해요', emoji: '🥰' },
      { key: 'stressed', label: '스트레스!', emoji: '🤯' },
    ]

    // 인기 영화 가져오기
    const fetchPopularMovies = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/popular/')
        popularMovies.value = response.data
      } catch (error) {
        console.error('인기 영화 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    const getImageUrl = (path) => {
      if (!path) return '/assets/no-poster.png'
      return `https://image.tmdb.org/t/p/w500${path}`
    }

    const goToMovieDetail = (movieId) => {
      router.push(`/movies/${movieId}`)
    }

    const selectMood = (mood) => {
      showMoodModal.value = false

      // 로그인 상태 확인 (Pinia Store 사용)
      if (!authStore.isAuthenticated) {
        if(confirm('로그인이 필요한 서비스입니다. 로그인 페이지로 이동하시겠습니까?')) {
            router.push('/login')
        }
        return
      }
      
      // 추천 페이지로 이동
      router.push({ name: 'recommend', query: { mood: mood } })
    }

    const closeModal = () => {
      showMoodModal.value = false
    }

	// [추가] 검색어 상태
    const keyword = ref('')

    // [추가] 검색 실행 함수 (엔터 치거나 버튼 누르면 실행)
    const onSearch = () => {
      if (keyword.value.trim()) {
        // 단순하게 /search 페이지로 이동만 시킵니다.
        // 쿼리 파라미터 q에 검색어를 담아 보냅니다.
        router.push({ name: 'search', query: { q: keyword.value } })
      }
    }

    onMounted(() => {
      fetchPopularMovies()
      
      // [수정] 로그인한 유저라면 들어오자마자 모달 띄우기
      if (authStore.isAuthenticated) {
        showMoodModal.value = true
      }
    })

    return {
      popularMovies,
      loading,
      goToMovieDetail,
      showMoodModal,
      selectMood,
      closeModal,
      getImageUrl,
      moodOptions, // 템플릿 사용을 위해 반환
      authStore,
	  	keyword,
      onSearch
    }
  }
}
</script>

<style scoped>
/* 기존 스타일 유지 */
.home-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
  position: relative;
}

.welcome-section { margin-bottom: 4rem; text-align: center; }
.welcome-content { max-width: 800px; margin: 0 auto; }
.welcome-title { font-size: 2.5rem; font-weight: bold; color: #000000; margin-bottom: 1rem; }
.welcome-subtitle { font-size: 1.2rem; color: #000000; margin-bottom: 2rem; }
.popular-movies-section { margin-top: 4rem; }
.section-title { font-size: 2rem; font-weight: bold; color: #000000; margin-bottom: 0.5rem; }
.section-subtitle { font-size: 1rem; color: #000000; margin-bottom: 2rem; }
.loading-spinner { padding: 3rem 0; }
.movies-scroll-container { overflow-x: auto; overflow-y: hidden; padding-bottom: 1rem; }
.movies-grid { display: flex; gap: 1.5rem; padding-bottom: 1rem; }
.movie-card-item { flex-shrink: 0; width: 280px; cursor: pointer; }
.movie-card { background-color: #ffffff; border: 1px solid #000000; overflow: hidden; }
.movie-poster { width: 100%; height: 400px; object-fit: cover; display: block; }

/* 모달 스타일 (수정됨) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px); /* 배경 블러 추가 */
}

.modal-content {
  background-color: white;
  padding: 3rem;
  border-radius: 15px;
  text-align: center;
  max-width: 600px; /* 너비 약간 증가 */
  width: 90%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.modal-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.modal-subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.mood-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap; /* [중요] 버튼이 많아져서 줄바꿈 허용 */
}

.btn-mood {
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 1px solid #000;
  background: white;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  min-width: 120px; /* 버튼 최소 너비 지정 */
}

.btn-mood:hover {
  background: #000;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.emoji {
  margin-right: 5px;
}

.btn-close-modal {
  background: none;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  color: #666;
}

/* [추가] 검색창 스타일 */
.search-section {
  max-width: 600px;
  margin: 0 auto;
}
.search-form {
  display: flex;
  gap: 10px;
}
.search-input {
  border-radius: 50px;
  padding: 1rem 1.5rem;
  border: 2px solid #000;
}
.search-btn {
  border-radius: 5px;
  padding: 0 0.2rem;
  font-weight: bold;
	width: 5rem;
}
</style>