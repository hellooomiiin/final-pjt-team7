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
            <div class="d-flex align-items-center gap-3 mb-2">
              <h1 class="movie-title mb-0">{{ movie.title }}</h1>
              
              <button 
                @click="toggleLike" 
                class="btn-like" 
                :class="{ 'liked': isLiked }"
                title="찜하기"
              >
                <span v-if="isLiked" class="heart-icon">❤️</span>
                <span v-else class="heart-icon">🤍</span>
                <span class="like-count" v-if="likeCount > 0">{{ likeCount }}</span>
              </button>
            </div>

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

        <div class="reviews-section mt-5 pt-4 border-top">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="section-title mb-0">리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }})</h3>
            <div class="d-flex gap-2 align-items-center">
              <button 
                v-if="authStore.isAuthenticated"
                @click="goReviewCreate"
                class="btn btn-sm btn-review-create"
              >
                리뷰 작성하기
              </button>
              <router-link 
                :to="{ name: 'movie-reviews', params: { id: movie.tmdb_id } }" 
                class="btn btn-sm btn-outline-dark"
              >
                전체보기 &rarr;
              </router-link>
            </div>
          </div>

          <div v-if="!movie.review_set || movie.review_set.length === 0" class="alert alert-light text-center border py-4">
            <p class="text-muted mb-0">아직 작성된 리뷰가 없습니다. 첫 번째 리뷰를 남겨보세요!</p>
          </div>

          <div v-else class="row">
            <div
              v-for="review in movie.review_set.slice(0, 3)"
              :key="review.id"
              class="col-md-4 mb-3"
            >
              <div 
                class="card h-100 shadow-sm hover-effect border-0 bg-light"
                style="cursor: pointer;"
                @click="$router.push({ name: 'review-detail', params: { id: movie.tmdb_id, reviewId: review.id } })"
              >
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-warning text-dark small">★ {{ review.rank }}</span>
                    <small class="text-muted">{{ formatDate(review.created_at) }}</small>
                  </div>
                  <h5 class="card-title text-truncate fw-bold">{{ review.title }}</h5>
                  <p class="card-text text-muted small text-break" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                    {{ review.content }}
                  </p>
                  <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top">
                    <span class="small fw-bold">by {{ review.user_nickname || review.user }}</span>
                    <div class="small text-muted">
                      <span class="me-2">❤ {{ review.like_count || 0 }}</span>
                      <span>💬 {{ review.comments ? review.comments.length : 0 }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
import { ref, onMounted, computed } from 'vue' // computed 추가
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'MovieDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const movie = ref(null)
    const loading = ref(true)
    const trailerVideoId = ref(null)

    // [추가] 찜하기 관련 상태
    const isLiked = ref(false)
    const likeCount = ref(0)

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const goReviewDetail = (reviewId) => {
      if (!movie.value) return
      router.push({ 
        name: 'review-detail', 
        params: { id: movie.value.tmdb_id, reviewId: reviewId } 
      })
    }

    const goReviewCreate = async () => {
      if (!movie.value) return
      
      try {
        if (!authStore.user) await authStore.fetchProfile()
        
        const response = await axios({
          method: 'get',
          url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
          params: { movie: movie.value.id },
          headers: { Authorization: `Bearer ${authStore.token}` }
        })
        
        const currentUsername = authStore.user?.username
        const reviews = response.data.results || response.data
        const hasMyReview = Array.isArray(reviews) && reviews.some(
          review => review.user === currentUsername
        )
        
        if (hasMyReview) {
          alert('이미 이 영화에 리뷰를 작성하셨습니다.')
          return
        }
      } catch (error) {
        console.error('리뷰 확인 중 오류:', error)
      }
      
      router.push({ 
        name: 'review-create', 
        params: { id: movie.value.tmdb_id } 
      })
    }

    // [추가] 찜하기 토글 함수
    const toggleLike = async () => {
      // 1. 로그인 확인
      if (!authStore.isAuthenticated) {
        alert('로그인이 필요한 기능입니다.')
        router.push('/login')
        return
      }

      try {
        // 2. 백엔드 API 호출 (POST /movies/<db_id>/likes/)
        // 주의: TMDB ID가 아니라 DB의 PK(id)를 사용해야 합니다.
        const response = await axios({
          method: 'post',
          url: `http://127.0.0.1:8000/api/v1/movies/${movie.value.id}/likes/`,
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })

        // 3. 응답 받아서 상태 업데이트
        isLiked.value = response.data.is_liked
        likeCount.value = response.data.count

      } catch (error) {
        console.error('찜하기 실패:', error)
      }
    }

    const getImageUrl = (path, type = 'poster') => {
      if (!path) return type === 'actor' ? '/assets/no-profile.png' : '/assets/no-poster.png'
      const size = type === 'actor' ? 'w185' : 'w500'
      return `https://image.tmdb.org/t/p/${size}${path}`
    }

    const fetchTrailer = async (query) => {
      const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
      if (!YOUTUBE_API_KEY) return

      try {
        const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
          params: {
            part: 'snippet',
            q: `${query} 공식 예고편`,
            type: 'video',
            key: YOUTUBE_API_KEY,
            maxResults: 1
          }
        })

        if (response.data.items.length > 0) {
          trailerVideoId.value = response.data.items[0].id.videoId
        }
      } catch (error) {
        console.error('유튜브 예고편 로드 실패:', error)
      }
    }

    const fetchMovieDetail = async () => {
      loading.value = true
      try {
        const movieId = route.params.id
        const movieResponse = await axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/`)
        movie.value = movieResponse.data
        
        // [추가] 영화 정보 로드 후 찜 상태 초기화
        if (movie.value) {
            // like_users 배열이 있는지 확인 (백엔드 Serializer에 따라 다를 수 있음)
            const likeUsers = movie.value.like_users || []
            likeCount.value = likeUsers.length

            // 내가 찜했는지 확인
            if (authStore.user && authStore.isAuthenticated) {
                // like_users가 ID(숫자) 목록인 경우
                if (likeUsers.length > 0 && typeof likeUsers[0] === 'number') {
                    isLiked.value = likeUsers.includes(authStore.user.pk || authStore.user.id)
                } 
                // like_users가 객체 목록인 경우 (Serializer 설정에 따라)
                else {
                    isLiked.value = likeUsers.some(u => u.id === (authStore.user.pk || authStore.user.id))
                }
            } else {
                isLiked.value = false
            }

            // ... 기존 리뷰 및 예고편 로직 ...
            try {
                const reviewsResponse = await axios({
                method: 'get',
                url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
                params: { movie: movie.value.id }
                })
                if (!movie.value.review_set) {
                    movie.value.review_set = reviewsResponse.data.results || reviewsResponse.data
                }
            } catch (reviewError) {
                if (!movie.value.review_set) movie.value.review_set = []
            }
            await fetchTrailer(movie.value.title)
        }
      } catch (error) {
        console.error('영화 상세 정보 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
        // [추가] 유저 정보가 없으면 로드 시도 (찜 확인용)
        if (!authStore.user && authStore.token) {
            authStore.fetchProfile().then(() => {
                fetchMovieDetail()
            })
        } else {
            fetchMovieDetail()
        }
    })

    return {
      movie,
      loading,
      trailerVideoId,
      authStore,
      getImageUrl,
      formatDate,
      goReviewDetail,
      goReviewCreate,
      // [추가] 찜하기 관련 반환
      isLiked,
      likeCount,
      toggleLike
    }
  }
}
</script>

<style scoped>
/* [추가] 찜하기 버튼 스타일 */
.btn-like {
  background: none;
  border: 1px solid #ddd;
  border-radius: 50px; /* 둥근 버튼 */
  padding: 0.3rem 0.8rem;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  height: 40px;
}

.btn-like:hover {
  background-color: #f8f9fa;
  transform: scale(1.05);
  border-color: #000;
}

.btn-like.liked {
  border-color: #ff4757;
  background-color: #fff0f1;
}

.heart-icon {
  line-height: 1;
  font-size: 1.3rem;
}

.like-count {
  font-size: 1rem;
  font-weight: bold;
  color: #555;
}

/* 기존 스타일 그대로 유지 */
.movie-detail-container {
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
  padding: 3rem 0;
  color: #000000;
}
/* ... (나머지 스타일 생략 - 기존과 동일) ... */
.loading-spinner { padding: 5rem 0; }
.movie-poster-large { width: 100%; max-width: 400px; height: auto; border: 1px solid #000000; box-shadow: 10px 10px 0px rgba(0,0,0,0.1); }
.movie-title { font-size: 2.5rem; font-weight: bold; color: #000000; margin-bottom: 0; /* margin 수정 */ }
.movie-original-title { font-size: 1.2rem; color: #666666; margin-bottom: 2rem; }
.movie-overview { font-size: 1.1rem; line-height: 1.8; color: #000000; margin-bottom: 2rem; }
.movie-meta { display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 2rem; padding: 1rem; border: 1px solid #000; background: #f8f9fa; }
.meta-item { font-weight: bold; }
.section-title { font-size: 1.8rem; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
.video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border: 1px solid #000; }
.video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.alert-info { background-color: #ffffff; border: 1px solid #000000; color: #000000; padding: 2rem; text-align: center; }
.actor-img { width: 80px; height: 80px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd; margin-bottom: 5px; }
.actor-card { width: 90px; }
.director-name { font-size: 1.1rem; }
.x-small { font-size: 0.8rem; }
.btn-review-create { border: none !important; outline: none !important; box-shadow: none !important; color: #000000; transition: opacity 0.2s ease; }
.btn-review-create:hover { opacity: 0.7; }
@media (max-width: 768px) { .movie-title { font-size: 1.8rem; } .movie-poster-large { margin-bottom: 2rem; } }
</style>