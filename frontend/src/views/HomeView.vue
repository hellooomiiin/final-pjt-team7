<template>
  <div class="home-container">
    <div v-if="showMoodModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button @click="closeModal" class="close-button">×</button>
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
      </div>
    </div>

    <!-- 상단 프로모션 배너 - Carousel -->
    <div v-if="!loading && top5Movies.length > 0" id="promoCarousel" class="carousel slide" data-bs-ride="false" data-bs-interval="false">
      <!-- Carousel Indicators -->
      <div class="carousel-indicators">
        <button
          v-for="(movie, index) in top5Movies"
          :key="movie.tmdb_id"
          type="button"
          :data-bs-target="'#promoCarousel'"
          :data-bs-slide-to="index"
          :class="{ active: index === 0 }"
          :aria-current="index === 0 ? 'true' : undefined"
          :aria-label="`Slide ${index + 1}`"
        ></button>
      </div>

      <!-- Carousel Items -->
      <div class="carousel-inner">
        <div
          v-for="(movie, index) in top5Movies"
          :key="movie.tmdb_id"
          class="carousel-item"
          :class="{ active: index === 0 }"
          :style="{ backgroundImage: `url(${getBackdropUrl(movie.poster_path)})` }"
          @click="goToMovieDetail(movie.tmdb_id)"
        >
          <div class="carousel-overlay"></div>
          <div class="carousel-content">
            <p class="carousel-subtitle carousel-subtitle-top">AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다</p>
            <p class="carousel-subtitle carousel-subtitle-bottom">지금 바로 나만의 맞춤 영화를 만나보세요</p>
            <button @click.stop="showMoodModal = true" class="btn-mood-select">
              감정 다시 선택하기
            </button>
          </div>
        </div>
      </div>

      <!-- Carousel Controls -->
      <button class="carousel-control-prev" type="button" data-bs-target="#promoCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#promoCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <!-- 로딩 중일 때 또는 영화가 없을 때 기본 배너 -->
    <div v-else class="promo-banner">
      <div class="promo-overlay"></div>
      <div class="promo-content">
        <h1 class="promo-title">AI가 당신의 기분을 분석하여<br>완벽한 영화를 추천해드립니다</h1>
        <p class="promo-subtitle">Mood-Match는 당신의 감정에 딱 맞는 영화를 찾아드립니다</p>
        <p class="promo-description">지금 바로 기분을 선택하고 나만의 맞춤 영화를 만나보세요</p>
        <button @click="showMoodModal = true" class="btn-mood-select">
          감정 다시 선택하기
        </button>
      </div>
    </div>

    <!-- 검색 섹션 -->
    <div class="search-section">
      <div class="search-container">
        <input
          v-model="keyword"
          @keyup.enter="onSearch"
          type="text"
          class="search-input"
          placeholder="영화 제목을 검색하세요..."
        />
      </div>
    </div>

    <div class="main-content">
      <!-- 인기 영화 섹션 -->
      <div class="popular-movies-section">
        <h2 class="section-title">인기영화 TOP 10</h2>
        
        <div v-if="loading" class="loading-spinner">
          <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else id="moviesCarousel" class="carousel slide" data-bs-ride="false" data-bs-interval="false">
          <!-- Carousel Indicators -->
          <div class="carousel-indicators movies-indicators">
            <button
              v-for="(page, index) in moviePages"
              :key="index"
              type="button"
              data-bs-target="#moviesCarousel"
              :data-bs-slide-to="index"
              :class="{ active: index === 0 }"
              :aria-current="index === 0 ? 'true' : undefined"
              :aria-label="`Slide ${index + 1}`"
            ></button>
          </div>

          <!-- Carousel Items -->
          <div class="carousel-inner movies-carousel-inner">
            <div
              v-for="(page, pageIndex) in moviePages"
              :key="pageIndex"
              class="carousel-item"
              :class="{ active: pageIndex === 0 }"
            >
              <div class="movies-grid">
                <div
                  v-for="(movie, index) in page"
                  :key="movie.tmdb_id"
                  class="movie-card"
                  @click="goToMovieDetail(movie.tmdb_id)"
                >
                  <div class="movie-rank">{{ pageIndex * 5 + index + 1 }}</div>
                  <div class="movie-thumbnail">
                    <img
                      :src="getImageUrl(movie.poster_path)"
                      :alt="movie.title"
                    />
                  </div>
                  <div class="movie-info">
                    <h3 class="movie-title">{{ movie.title }}</h3>
                    <div class="movie-details">
                      <span class="rating-badge" :class="getRatingClass(movie.vote_average)">
                        {{ getRatingText(movie.vote_average) }}
                      </span>
                      <span class="year">{{ getYear(movie.release_date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Carousel Controls -->
          <button class="carousel-control-prev movies-control" type="button" data-bs-target="#moviesCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next movies-control" type="button" data-bs-target="#moviesCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { ref, computed, onMounted } from 'vue'
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

    // Top 5 영화만 가져오기 (캐러셀용)
    const top5Movies = computed(() => {
      return popularMovies.value.slice(0, 5)
    })

    // Top 10 영화만 가져오기 (인기 영화 섹션용)
    const top10Movies = computed(() => {
      return popularMovies.value.slice(0, 10)
    })

    // 영화를 페이지별로 나누기 (한 페이지에 5개씩)
    const moviePages = computed(() => {
      const pages = []
      for (let i = 0; i < top10Movies.value.length; i += 5) {
        pages.push(top10Movies.value.slice(i, i + 5))
      }
      return pages
    })

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

    const getBackdropUrl = (path) => {
      if (!path) return 'https://image.tmdb.org/t/p/w1280/kqjL17yufvn9OVLyXYpvtyrFfak.jpg'
      // 배경용으로 더 큰 이미지 사용 (w1280 또는 w780)
      return `https://image.tmdb.org/t/p/w1280${path}`
    }

    const getYear = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).getFullYear()
    }

    const getRatingText = (rating) => {
      if (!rating) return 'ALL'
      if (rating >= 19) return '19'
      if (rating >= 15) return '15'
      if (rating >= 12) return '12'
      return 'ALL'
    }

    const getRatingClass = (rating) => {
      if (!rating) return 'rating-all'
      if (rating >= 19) return 'rating-19'
      if (rating >= 15) return 'rating-15'
      if (rating >= 12) return 'rating-12'
      return 'rating-all'
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
      top5Movies,
      top10Movies,
      moviePages,
      loading,
      goToMovieDetail,
      showMoodModal,
      selectMood,
      closeModal,
      getImageUrl,
      getBackdropUrl,
      getYear,
      getRatingText,
      getRatingClass,
      moodOptions,
      authStore,
	  	keyword,
      onSearch
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Thin.woff2') format('woff2');
  font-weight: 100;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-ExtraLight.woff2') format('woff2');
  font-weight: 200;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Light.woff2') format('woff2');
  font-weight: 300;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Regular.woff2') format('woff2');
  font-weight: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Medium.woff2') format('woff2');
  font-weight: 500;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-SemiBold.woff2') format('woff2');
  font-weight: 600;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Bold.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-ExtraBold.woff2') format('woff2');
  font-weight: 800;
  font-display: swap;
}

@font-face {
  font-family: 'Suit';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Heavy.woff2') format('woff2');
  font-weight: 900;
  font-display: swap;
}

.home-container {
  min-height: calc(100vh - 80px);
  background-color: #000000;
  color: #ffffff;
  position: relative;
}

/* Carousel 스타일 */
#promoCarousel {
  position: relative;
  width: 100%;
  max-width: 1330px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 500px;
  overflow: hidden;
}

.carousel-inner {
  height: 500px;
}

.carousel-item {
  position: relative;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
}

.carousel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.5) 50%,
    rgba(0, 0, 0, 0.8) 100%
  );
  z-index: 1;
}

.carousel-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  height: 100%;
  text-align: center;
  padding: 4rem 2rem 6rem;
  max-width: 1200px;
  margin: 0 auto;
}

.carousel-title {
  font-size: 3rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);
}

.carousel-subtitle {
  font-size: 2.6364rem;
  color: #ffffff;
  margin-bottom: 2.5rem;
  font-weight: 800;
  font-family: 'Suit', sans-serif;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.8);
  white-space: nowrap;
}

.carousel-subtitle-top {
  margin-bottom: 0.5rem;
}

.carousel-subtitle-bottom {
  font-size: 1.84548rem; /* 2.6364rem * 0.7 = 30% 감소 */
  font-weight: 500; /* 더 얇게 */
  margin-bottom: 2.5rem;
}

/* Carousel Indicators - Bootstrap 기본 스타일 */
.carousel-indicators {
  margin-bottom: 1rem;
  z-index: 3;
}

/* Carousel Controls 커스터마이징 */
.carousel-control-prev,
.carousel-control-next {
  width: 5%;
  opacity: 0.5;
  transition: opacity 0.3s ease;
  z-index: 3;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.carousel-control-prev:focus,
.carousel-control-next:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  opacity: 1;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background-color: transparent !important;
}

.carousel-control-prev:hover .carousel-control-prev-icon,
.carousel-control-next:hover .carousel-control-next-icon {
  background-color: rgba(0, 0, 0, 0.7) !important;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  background-size: 60% 60%;
  border: none !important;
  outline: none !important;
  filter: none !important;
}

/* 프로모션 배너 (로딩/기본용) */
.promo-banner {
  position: relative;
  width: 100%;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #000000 50%, #1a1a1a 100%);
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.promo-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.4) 0%,
    rgba(0, 0, 0, 0.6) 50%,
    rgba(0, 0, 0, 0.8) 100%
  );
  z-index: 1;
}

.promo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.8) 100%);
  z-index: 1;
}

.promo-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 4rem 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.promo-title {
  font-size: 3rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.promo-subtitle {
  font-size: 1.5rem;
  color: #ffffff;
  margin-bottom: 1rem;
  font-weight: 500;
}

.promo-description {
  font-size: 1.1rem;
  color: #cccccc;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.btn-mood-select {
  padding: 1rem 2rem;
  font-size: 1.44rem;
  font-weight: bold;
  background: linear-gradient(135deg, #FF1744 0%, #DC143C 50%, #C41E3A 100%);
  color: #ffffff;
  border: none !important;
  outline: none !important;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: none !important;
}

.btn-mood-select:hover {
  background: linear-gradient(135deg, #FF4569 0%, #FF1744 50%, #DC143C 100%);
  transform: translateY(-2px);
  box-shadow: none !important;
}

.btn-mood-select:focus {
  border: none !important;
  outline: none !important;
}

.btn-mood-select:active {
  border: none !important;
  outline: none !important;
}

.main-content {
  padding: 4rem 2rem;
  max-width: 1330px;
  margin: 0 auto;
}

/* 인기 영화 섹션 */
.popular-movies-section {
  margin-top: 2rem;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 2rem;
  padding-left: 0.5rem;
}

.loading-spinner {
  text-align: center;
  padding: 4rem 0;
}

/* 인기 영화 Carousel */
#moviesCarousel {
  position: relative;
  width: 100%;
  max-width: 1330px;
  margin: 0 auto;
  height: 500px;
  padding: 0 2rem;
}

.movies-carousel-inner {
  height: 500px;
  padding-bottom: 3rem;
}

.movies-grid {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: flex-start;
  padding: 0;
  height: 100%;
  width: 100%;
}

.movies-indicators {
  margin-bottom: 1rem;
  z-index: 3;
}

.movies-control {
  width: 5%;
  opacity: 0.5;
  transition: opacity 0.3s ease;
  z-index: 3;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.movies-control:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.movies-control:hover {
  opacity: 1;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background-color: transparent !important;
}

.movies-control:hover .carousel-control-prev-icon,
.movies-control:hover .carousel-control-next-icon {
  background-color: rgba(0, 0, 0, 0.7) !important;
}

.movies-control .carousel-control-prev-icon,
.movies-control .carousel-control-next-icon {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  background-size: 60% 60%;
  border: none !important;
  outline: none !important;
  filter: none !important;
}

.movie-card {
  position: relative;
  flex: 0 0 calc((100% - 4rem) / 5);
  max-width: calc((100% - 4rem) / 5);
  min-width: 0;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-8px) scale(1.02);
}

.movie-rank {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.8);
  color: #ffffff;
  font-size: 2rem;
  font-weight: bold;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  z-index: 2;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.movie-thumbnail {
  width: 100%;
  height: auto;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 1rem;
  background-color: #1a1a1a;
}

.movie-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.movie-card:hover .movie-thumbnail img {
  transform: scale(1.05);
}

.movie-info {
  padding: 0.5rem 0;
}

.movie-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.75rem;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.movie-details {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rating-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: bold;
  display: inline-block;
}

.rating-19 {
  background-color: #dc3545;
  color: #ffffff;
}

.rating-15 {
  background-color: #dc3545;
  color: #ffffff;
}

.rating-12 {
  background-color: #ffc107;
  color: #000000;
}

.rating-all {
  background-color: #28a745;
  color: #ffffff;
}

.year {
  color: #cccccc;
  font-size: 0.9rem;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background-color: #1a1a1a;
  padding: 22px;
  border-radius: 8px;
  text-align: center;
  max-width: 600px;
  width: 90%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #333333;
  border: none;
  color: #ffffff;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background-color 0.2s;
  z-index: 10;
}

.close-button:hover {
  background-color: #444444;
}

.close-button:focus {
  outline: none;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.modal-subtitle {
  color: #999999;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.mood-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 0;
  flex-wrap: wrap;
}

.btn-mood {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
  border: none;
  background-color: #333333;
  color: #ffffff;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
  min-width: 120px;
}

.btn-mood:hover {
  background-color: #444444;
  color: #ffffff;
}

.emoji {
  margin-right: 5px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  #promoCarousel,
  .promo-banner {
    min-height: 400px;
  }

  .carousel-inner {
    height: 400px;
  }

  .carousel-title,
  .promo-title {
    font-size: 2rem;
  }

  .carousel-subtitle,
  .promo-subtitle {
    font-size: 1.2rem;
  }

  .promo-description {
    font-size: 1rem;
  }

  .btn-mood-select {
    padding: 0.875rem 1.5rem;
    font-size: 1rem;
  }

  .carousel-control-prev-icon,
  .carousel-control-next-icon {
    width: 40px;
    height: 40px;
  }

  .main-content {
    padding: 2rem 1rem;
  }

  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  #moviesCarousel {
    padding: 0 1rem;
  }

  .movie-card {
    flex: 0 0 calc((100% - 2rem) / 2);
    max-width: calc((100% - 2rem) / 2);
  }
}

@media (max-width: 480px) {
  #promoCarousel,
  .promo-banner {
    min-height: 350px;
  }

  .carousel-inner {
    height: 350px;
  }

  .carousel-content,
  .promo-content {
    padding: 2rem 1rem;
  }

  .carousel-title,
  .promo-title {
    font-size: 1.5rem;
  }

  .carousel-subtitle,
  .promo-subtitle {
    font-size: 1rem;
  }

  .promo-description {
    font-size: 0.9rem;
  }


  .carousel-control-prev-icon,
  .carousel-control-next-icon {
    width: 35px;
    height: 35px;
  }

  #moviesCarousel {
    padding: 0 0.5rem;
  }

  .movie-card {
    flex: 0 0 calc((100% - 0.5rem) / 2);
    max-width: calc((100% - 0.5rem) / 2);
  }

  .movie-rank {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }
}

/* 검색 섹션 스타일 */
.search-section {
  padding: 2rem 2rem 1rem;
  max-width: 1330px;
  margin: 0 auto;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  background-color: #1a1a1a;
  color: #ffffff;
  border: 2px solid #333333;
  border-radius: 50px;
  outline: none;
  transition: all 0.3s ease;
  font-family: 'Suit', sans-serif;
}

.search-input::placeholder {
  color: #808080;
}

.search-input:focus {
  border-color: #E50914;
  background-color: #2a2a2a;
  box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.1);
}

.search-input:hover {
  border-color: #555555;
}

/* 반응형 */
@media (max-width: 768px) {
  .search-section {
    padding: 1.5rem 1rem 1rem;
  }

  .search-input {
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .search-section {
    padding: 1rem 0.5rem 0.5rem;
  }

  .search-input {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }
}
</style>