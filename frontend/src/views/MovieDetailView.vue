<template>
  <div class="movie-detail-container">
    <div class="container">
      <div v-if="loading" class="text-center loading-spinner">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="movie" class="movie-detail">
        <div class="row">
          <div class="col-md-4">
            <img
              :src="getImageUrl(movie.poster_path, 'poster')"
              class="movie-poster-large"
              :alt="movie.title"
            />
          </div>
          
          <div class="col-md-8">
            <h1 class="movie-title">{{ movie.title }}</h1>
            <p v-if="movie.original_title" class="movie-original-title">
              {{ movie.original_title }}
            </p>
            
            <div class="movie-info">
              <p v-if="movie.overview" class="movie-overview">{{ movie.overview }}</p>
              
              <div class="movie-meta">
                <span v-if="movie.release_date" class="meta-item">
                  개봉일: {{ movie.release_date }}
                </span>
                <span v-if="movie.runtime" class="meta-item">
                  상영시간: {{ movie.runtime }}분
                </span>
                <span v-if="movie.vote_average" class="meta-item">
                  평점: {{ movie.vote_average.toFixed(1) }}/10
                </span>
                <span v-if="movie.popularity" class="meta-item">
                  인기도: {{ movie.popularity.toFixed(0) }}
                </span>
              </div>

              <div class="people-info mt-4">
                <div v-if="movie.director" class="mb-3">
                  <strong>감독:</strong> <span class="director-name">{{ movie.director }}</span>
                </div>

                <div v-if="movie.actors && movie.actors.length" class="actors-list">
                  <strong>출연:</strong>
                  <div class="d-flex flex-wrap gap-3 mt-2">
                    <div v-for="actor in movie.actors" :key="actor.name" class="actor-card text-center">
                      <img 
                        :src="getImageUrl(actor.profile_path, 'actor')" 
                        class="actor-img" 
                        alt="actor"
                      >
                      <div class="actor-name small mt-1">{{ actor.name }}</div>
                      <div class="actor-char x-small text-muted">{{ actor.character }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="movie.genres && movie.genres.length" class="mt-3">
                <span v-for="genre in movie.genres" :key="genre.tmdb_id" class="badge bg-secondary me-1">
                  {{ genre.name }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="trailerVideoId" class="trailer-section mt-5">
          <h3 class="section-title mb-3">예고편</h3>
          <div class="video-container">
            <iframe
              :src="`https://www.youtube.com/embed/${trailerVideoId}`"
              title="YouTube video player"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>

        <div class="reviews-section mt-5">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="section-title">리뷰</h3>
            </div>
          
          <div v-if="reviews.length === 0" class="alert alert-info">
            아직 작성된 리뷰가 없습니다. 첫 번째 리뷰를 남겨보세요!
          </div>
          
          <div v-else>
             </div>
        </div>

      </div>

      <div v-else class="alert alert-info">
        영화 정보를 찾을 수 없습니다.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'MovieDetailView',
  setup() {
    const route = useRoute()
    const movie = ref(null)
    const loading = ref(true)
    const reviews = ref([]) // 리뷰 데이터 (추후 구현)
    
    // 유튜브 관련 상태
    const trailerVideoId = ref(null)

    // 1. Django API에서 영화 상세 정보 가져오기
    const fetchMovieDetail = async () => {
      try {
        const movieId = route.params.id // URL의 movie_id
        // 백엔드 주소
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/`)
        movie.value = response.data
        
        // 영화 정보를 다 가져온 후 -> 유튜브 검색 시작
        if (movie.value) {
          await fetchTrailer(movie.value.title)
        }

      } catch (error) {
        console.error('영화 상세 정보 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    // 2. YouTube API로 예고편 검색하기
    const fetchTrailer = async (query) => {
      const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
      
      try {
        const searchResponse = await axios.get('https://www.googleapis.com/youtube/v3/search', {
          params: {
            part: 'snippet',
            q: `${query} 공식 예고편`, // 검색어: "영화제목 + 공식 예고편"
            type: 'video',
            key: YOUTUBE_API_KEY,
            maxResults: 1
          }
        })

        if (searchResponse.data.items.length > 0) {
          trailerVideoId.value = searchResponse.data.items[0].id.videoId
        }
      } catch (error) {
        console.error('유튜브 예고편 로드 실패:', error)
      }
    }

    // 3. 이미지 URL 생성 헬퍼
    const getImageUrl = (path, type = 'poster') => {
      // 1. 이미지가 없을 경우 (null 또는 빈 문자열)
      if (!path) {
        if (type === 'actor') {
          return '/assets/no-profile.png' // 배우용 기본 이미지 (사람 실루엣 등)
        }
        return '/assets/no-poster.png'   // 영화용 기본 이미지 (회색 박스 등)
      }

      // 2. 이미지가 있을 경우 (크기 최적화)
      // 배우 사진은 작아도 되니까 w185나 w200으로 설정
      const size = type === 'actor' ? 'w185' : 'w500'
      
      return `https://image.tmdb.org/t/p/${size}${path}`
    }

    onMounted(() => {
      fetchMovieDetail()
      // fetchReviews() // 백엔드에 리뷰 API가 생기면 주석 해제
    })

    return {
      movie,
      loading,
      reviews,
      getImageUrl,
      trailerVideoId
    }
  }
}
</script>

<style scoped>
.movie-detail-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}

.loading-spinner {
  padding: 5rem 0;
}

.movie-poster-large {
  width: 100%;
  max-width: 400px;
  height: auto;
  border: 1px solid #000000;
  box-shadow: 10px 10px 0px rgba(0,0,0,0.1); /* 스타일 추가 */
}

.movie-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000000;
  margin-bottom: 0.5rem;
}

.movie-original-title {
  font-size: 1.2rem;
  color: #666666;
  margin-bottom: 2rem;
}

.movie-overview {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #000000;
  margin-bottom: 2rem;
}

.movie-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #000;
  background: #f8f9fa;
}

.meta-item {
  font-weight: bold;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  border-bottom: 2px solid #000;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

/* 비디오 반응형 컨테이너 */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
  border: 1px solid #000;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.alert-info {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 2rem;
  text-align: center;
}

.actor-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 50%; /* 동그란 프로필 사진 */
  border: 1px solid #ddd;
  margin-bottom: 5px;
}

.actor-card {
  width: 90px;
}

.director-name {
  font-size: 1.1rem;
}

.x-small {
  font-size: 0.8rem;
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .movie-title { font-size: 1.8rem; }
  .movie-poster-large { margin-bottom: 2rem; }
}
</style>