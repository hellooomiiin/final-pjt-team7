<template>
  <div class="home-container">
    <div v-if="showMoodModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title">오늘의 기분은 어떠신가요?</h3>
        <p class="modal-subtitle">기분에 딱 맞는 영화를 추천해 드릴게요.</p>
        
        <div class="mood-buttons">
          <button @click="selectMood('bored')" class="btn-mood">🥱 심심함</button>
          <button @click="selectMood('angry')" class="btn-mood">😡 화나는</button>
          <button @click="selectMood('sad')" class="btn-mood">😢 슬픈</button>
        </div>
        
        <button class="btn-close-modal" @click="closeModal">닫기</button>
      </div>
    </div>
    <div class="container">
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">
            <span class="check-icon">✓</span>
            Mood-Match에 오신 것을 환영합니다
          </h1>
          <p class="welcome-subtitle">
            AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다
          </p>
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
              :key="movie.id"
              class="movie-card-item"
              @click="goToMovieDetail(movie.id)"
            >
              <div class="movie-card">
                <img
                  :src="movie.poster_path || '/placeholder.jpg'"
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { mockApi } from '@/data/mockData'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    const popularMovies = ref([])
    const loading = ref(true)
    
    // ▼▼▼ 추가된 상태 변수들 ▼▼▼
    const showMoodModal = ref(false)
    // 실제 앱에서는 스토어(Pinia)에서 로그인 상태를 가져와야 합니다.
    const isLoggedIn = ref(true) // 테스트를 위해 true로 설정

    const fetchPopularMovies = async () => {
      try {
        const response = await mockApi.getPopularMovies()
        popularMovies.value = response.data
      } catch (error) {
        console.error('인기 영화 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    const goToMovieDetail = (movieId) => {
      router.push(`/movies/${movieId}`)
    }

    // ▼▼▼ 추가된 함수들 ▼▼▼
    const selectMood = (mood) => {
      showMoodModal.value = false
      // 선택한 감정을 쿼리 파라미터로 넘기며 추천 페이지로 이동
      router.push({ name: 'recommend', query: { mood: mood } })
    }

    const closeModal = () => {
      showMoodModal.value = false
    }

    onMounted(() => {
      fetchPopularMovies()
      
      // 로그인이 되어 있다면 팝업 띄우기
      if (isLoggedIn.value) {
        showMoodModal.value = true
      }
    })

    return {
      popularMovies,
      loading,
      goToMovieDetail,
      showMoodModal,  // 추가
      selectMood,     // 추가
      closeModal      // 추가
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
  position: relative; /* 모달 위치 잡기 위해 추가 */
}

/* ... (기존 스타일 생략: welcome-section 등 그대로 두세요) ... */
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

/* ▼▼▼ 모달 관련 스타일 추가 ▼▼▼ */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 검은 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 3rem;
  border-radius: 15px;
  text-align: center;
  max-width: 500px;
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
}

.btn-mood {
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 1px solid #000;
  background: white;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.btn-mood:hover {
  background: #000;
  color: white;
  transform: translateY(-2px);
}

.btn-close-modal {
  background: none;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  color: #666;
}
</style>