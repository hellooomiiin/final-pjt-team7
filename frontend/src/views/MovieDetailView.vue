<template>
  <div class="movie-detail-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="movie" class="movie-detail">
      <!-- 히어로 섹션 -->
      <div 
        class="hero-section"
        :style="{ backgroundImage: `url(${getBackdropUrl(movie.poster_path)})` }"
      >
        <div class="hero-overlay"></div>
        <div class="hero-content">
          <h1 class="hero-title">{{ movie.title }}</h1>
          <p v-if="movie.original_title && movie.original_title !== movie.title" class="hero-subtitle">
            {{ movie.original_title }}
          </p>
          <div class="hero-meta">
            <span v-if="movie.release_date" class="meta-year">{{ getYear(movie.release_date) }}</span>
            <span class="meta-separator">·</span>
            <span v-if="movie.genres && movie.genres.length" class="meta-genres">
              {{ movie.genres.map(g => g.name).join('/') }}
            </span>
          </div>
          <div class="hero-details">
            <span v-if="movie.runtime" class="detail-item">
              {{ formatRuntime(movie.runtime) }}
            </span>
            <span class="detail-separator">·</span>
            <span class="detail-rating">{{ getRatingText(movie.vote_average) }}</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 -->
      <div class="main-content-wrapper">
        <div class="poster-synopsis-layout">
          <!-- 포스터 -->
          <div class="poster-container">
            <img
              :src="getImageUrl(movie.poster_path, 'poster')"
              class="movie-poster"
              :alt="movie.title"
            />
          </div>
          <!-- 줄거리 및 평점/찜하기 -->
          <div class="synopsis-section">
            <!-- TMDB 별점, 평균 별점, 찜하기 버튼 -->
            <div class="rating-action-section">
              <div class="rating-info">
                <div class="rating-value">★ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</div>
                <div class="rating-label">
                  TMDB 평점<span v-if="movie.vote_count">({{ formatVoteCount(movie.vote_count) }})</span>
                </div>
              </div>
              <div class="action-buttons-group">
              <button @click="toggleLike" class="action-btn" :class="{ 'active': isLiked }">
                <span v-if="!isLiked" class="action-icon">+</span>
                <span v-else class="action-icon">✔</span>
                <span class="action-text">{{ isLiked ? '찜완료' : '찜하기' }}</span>
              </button>
                <button @click="scrollToReviews" class="action-btn">
                  <span class="action-text">후기 보기</span>
                </button>
                <button v-if="trailerVideoId" @click="scrollToTrailer" class="action-btn">
                  <span class="action-text">예고편 보기</span>
                </button>
              </div>
            </div>
            <!-- 줄거리 -->
            <h2 class="synopsis-title">줄거리</h2>
            <p v-if="movie.overview" class="synopsis-text">{{ movie.overview }}</p>
            <p v-else class="synopsis-text">줄거리 정보가 없습니다.</p>
          </div>
        </div>

        <!-- 출연/제작 정보 -->
        <div class="cast-crew-section">
          <h3 class="section-title">출연/제작</h3>
          <div v-if="castPages.length > 0" id="castCarousel" class="carousel slide" data-bs-ride="false" data-bs-interval="false">
            <!-- Carousel Indicators -->
            <div v-if="castPages.length > 1" class="carousel-indicators">
              <button
                v-for="(page, index) in castPages"
                :key="index"
                type="button"
                data-bs-target="#castCarousel"
                :data-bs-slide-to="index"
                :class="{ active: index === 0 }"
                :aria-current="index === 0 ? 'true' : undefined"
                :aria-label="`Slide ${index + 1}`"
              ></button>
            </div>

            <!-- Carousel Items -->
            <div class="carousel-inner">
              <div
                v-for="(page, pageIndex) in castPages"
                :key="pageIndex"
                class="carousel-item"
                :class="{ active: pageIndex === 0 }"
              >
                <div class="cast-grid">
                  <div
                    v-for="(person, index) in page"
                    :key="person.key || index"
                    class="cast-item"
                  >
                    <div class="cast-avatar">
                      <img
                        v-if="person.profile_path"
                        :src="getImageUrl(person.profile_path, 'actor')"
                        :alt="person.name"
                      />
                      <img
                        v-else
                        :src="noImgPeople"
                        :alt="person.name"
                        class="cast-no-image"
                      />
                    </div>
                    <div class="cast-info">
                      <div class="cast-name">{{ person.name }}</div>
                      <div class="cast-role">{{ person.role }}</div>
                      <div v-if="person.character" class="cast-character">{{ person.character }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Carousel Controls -->
            <button v-if="castPages.length > 1" class="carousel-control-prev" type="button" data-bs-target="#castCarousel" data-bs-slide="prev"></button>
            <button v-if="castPages.length > 1" class="carousel-control-next" type="button" data-bs-target="#castCarousel" data-bs-slide="next"></button>
          </div>
        </div>

        <!-- 예고편 섹션 -->
        <div v-if="trailerVideoId" id="trailer-section" class="trailer-section">
          <h3 class="section-title">예고편</h3>
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

        <!-- 리뷰 섹션 -->
        <div id="reviews-section" class="reviews-section">
          <div class="reviews-header">
            <h3 class="section-title">리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }})</h3>
            <div class="reviews-actions">
              <button 
                v-if="authStore.isAuthenticated"
                @click="goReviewCreate"
                class="btn-review-create"
              >
                리뷰 작성하기
              </button>
              <router-link 
                :to="{ name: 'movie-reviews', params: { id: movie.tmdb_id } }" 
                class="btn-view-all"
              >
                전체보기 →
              </router-link>
            </div>
          </div>

          <div v-if="!movie.review_set || movie.review_set.length === 0" class="no-reviews">
            <p>아직 작성된 리뷰가 없습니다. 첫 번째 리뷰를 남겨보세요!</p>
          </div>

          <div v-else class="reviews-grid">
            <div
              v-for="review in movie.review_set.slice(0, 3)"
              :key="review.id"
              class="review-card"
              @click="$router.push({ name: 'review-detail', params: { id: movie.tmdb_id, reviewId: review.id } })"
            >
              <div class="review-header">
                <span class="review-rating">★ {{ review.rank }}</span>
                <span class="review-date">{{ formatDate(review.created_at) }}</span>
              </div>
              <h4 class="review-title">{{ review.title }}</h4>
              <p class="review-content">{{ review.content }}</p>
              <div class="review-footer">
                <span class="review-author">by {{ review.user_nickname || review.user }}</span>
                <div class="review-stats">
                  <span>❤ {{ review.like_count || 0 }}</span>
                  <span>💬 {{ review.comments ? review.comments.length : 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-message">
      영화 정보를 찾을 수 없습니다.
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue' // computed 추가
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import noImgPeople from '@/assets/no_img_people.png'

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

    const scrollToReviews = () => {
      const reviewsSection = document.getElementById('reviews-section')
      if (reviewsSection) {
        reviewsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }

    const scrollToTrailer = () => {
      const trailerSection = document.getElementById('trailer-section')
      if (trailerSection) {
        trailerSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }

    const getImageUrl = (path, type = 'poster') => {
      if (!path) return type === 'actor' ? '/assets/no-profile.png' : '/assets/no-poster.png'
      const size = type === 'actor' ? 'w185' : 'w500'
      return `https://image.tmdb.org/t/p/${size}${path}`
    }

    const getBackdropUrl = (path) => {
      if (!path) return 'https://image.tmdb.org/t/p/w1280/kqjL17yufvn9OVLyXYpvtyrFfak.jpg'
      return `https://image.tmdb.org/t/p/w1280${path}`
    }

    const getYear = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).getFullYear()
    }

    const formatRuntime = (minutes) => {
      if (!minutes) return ''
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0) {
        return `${hours}시간 ${mins}분`
      }
      return `${mins}분`
    }

    const getRatingText = (rating) => {
      if (!rating) return 'ALL'
      if (rating >= 19) return '19'
      if (rating >= 15) return '15'
      if (rating >= 12) return '12'
      return 'ALL'
    }

    const formatVoteCount = (count) => {
      if (!count) return ''
      if (count >= 10000) {
        return `${(count / 10000).toFixed(1)}만명`
      }
      return `${count}명`
    }

    // 별점 분포 계산 (vote_average를 기반으로 가상 분포 생성)
    const ratingDistribution = computed(() => {
      if (!movie.value || !movie.value.vote_average) {
        return []
      }

      const avg = movie.value.vote_average / 2 // TMDB는 10점 만점이므로 5점 만점으로 변환
      const ratings = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
      
      // 평균을 중심으로 정규분포 형태의 가상 데이터 생성
      const distribution = ratings.map(rating => {
        // 평균에 가까울수록 높은 값 (정규분포 형태)
        const distance = Math.abs(rating - avg)
        // 표준편차를 1.0으로 가정한 정규분포
        const stdDev = 1.0
        const exponent = -0.5 * Math.pow(distance / stdDev, 2)
        const percentage = Math.max(10, Math.exp(exponent) * 100)
        return {
          rating: rating.toFixed(1),
          percentage: percentage
        }
      })

      // 가장 높은 막대를 찾아서 정규화 (최대값을 100%로)
      const maxPercentage = Math.max(...distribution.map(d => d.percentage))
      return distribution.map(d => ({
        ...d,
        percentage: maxPercentage > 0 ? (d.percentage / maxPercentage) * 100 : 0
      }))
    })

    // 출연/제작진을 8개씩 페이지로 나누기 (2열 4행)
    const castPages = computed(() => {
      if (!movie.value) return []
      
      const castList = []
      
      // 감독 추가
      if (movie.value.director) {
        castList.push({
          key: 'director',
          name: movie.value.director,
          role: '감독',
          profile_path: null
        })
      }
      
      // 배우 추가
      if (movie.value.actors && Array.isArray(movie.value.actors)) {
        movie.value.actors.forEach(actor => {
          castList.push({
            key: `actor-${actor.name}`,
            name: actor.name,
            role: '주연',
            character: actor.character,
            profile_path: actor.profile_path
          })
        })
      }
      
      // 8개씩 페이지로 나누기
      const pages = []
      for (let i = 0; i < castList.length; i += 8) {
        pages.push(castList.slice(i, i + 8))
      }
      
      return pages
    })

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
      getBackdropUrl,
      getYear,
      formatRuntime,
      getRatingText,
      formatVoteCount,
      formatDate,
      goReviewDetail,
      goReviewCreate,
      isLiked,
      likeCount,
      toggleLike,
      ratingDistribution,
      castPages,
      scrollToReviews,
      scrollToTrailer,
      noImgPeople
    }
  }
}
</script>

<style scoped>
.movie-detail-container {
  min-height: calc(100vh - 80px);
  background-color: #000000;
  color: #ffffff;
}

.loading-spinner {
  padding: 5rem 0;
  text-align: center;
}

.error-message {
  padding: 5rem 2rem;
  text-align: center;
  color: #ffffff;
  font-size: 1.2rem;
}

/* 폰트 정의 */
@font-face {
  font-family: 'Aggravo';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/SBAggroL.woff') format('woff');
  font-weight: 300;
  font-display: swap;
}

@font-face {
  font-family: 'Aggravo';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/SBAggroM.woff') format('woff');
  font-weight: 500;
  font-display: swap;
}

@font-face {
  font-family: 'Aggravo';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/SBAggroB.woff') format('woff');
  font-weight: 700;
  font-display: swap;
}

/* 히어로 섹션 */
.hero-section {
  position: relative;
  width: 100%;
  min-height: 500px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: flex-end;
  padding: 4rem 2rem 4rem 2rem;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.6) 50%,
    rgba(0, 0, 0, 0.9) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1330px;
  margin: 0 auto;
  width: 100%;
}

.hero-title {
  font-size: 4rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
}

.hero-subtitle {
  font-size: 1.5rem;
  color: #ffffff;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #ffffff;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.meta-year,
.meta-genres,
.meta-country {
  color: #ffffff;
}

.meta-separator {
  color: #ffffff;
  opacity: 0.7;
}

.hero-details {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #ffffff;
  flex-wrap: wrap;
}

.detail-item,
.detail-rating {
  color: #ffffff;
}

.detail-separator {
  color: #ffffff;
  opacity: 0.7;
}

/* 평점 및 액션 섹션 (줄거리 위) */
.rating-action-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
  gap: 1rem;
}

.action-buttons-group {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.rating-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
}

.rating-value {
  font-family: 'Aggravo', sans-serif;
  font-size: 3.2rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.rating-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.action-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  background-color: rgba(25, 25, 25, 0.7);
  border: none !important;
  outline: none !important;
  color: #ffffff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  min-width: 160px;
  width: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.action-btn:focus,
.action-btn:focus-visible,
.action-btn:active {
  border: none !important;
  outline: none !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 50%, rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  opacity: 0.7;
}

.action-btn::after {
  content: '';
  position: absolute;
  top: 1px;
  left: 1px;
  right: 1px;
  height: 50%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.1), transparent);
  border-radius: 12px 12px 0 0;
  pointer-events: none;
}

.action-btn:hover {
  background-color: rgba(30, 30, 30, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.action-btn.active {
  background-color: rgba(25, 25, 25, 0.7);
}

.action-btn.active::before {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 50%, rgba(255, 255, 255, 0) 100%);
  opacity: 0.7;
}

.action-icon {
  font-size: 1.5rem;
  font-weight: 300;
  line-height: 1;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5), 0 0 1px rgba(255, 255, 255, 0.3);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4));
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

.action-text {
  font-size: 0.95rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5), 0 0 1px rgba(255, 255, 255, 0.2);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4));
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

/* 메인 콘텐츠 */
.main-content-wrapper {
  max-width: 1330px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

/* 포스터 및 줄거리 레이아웃 */
.poster-synopsis-layout {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
  align-items: flex-start;
}

.poster-container {
  flex-shrink: 0;
}

.movie-poster {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  margin-bottom: 2rem;
}


.synopsis-section {
  color: #ffffff;
}

.synopsis-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.synopsis-text {
  font-size: 1rem;
  color: #cccccc;
  line-height: 1.8;
  white-space: pre-wrap;
}

/* 출연/제작 섹션 */
.cast-crew-section {
  color: #ffffff;
  margin-top: 4rem;
}

.cast-crew-section .section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

/* 출연/제작 Carousel */
#castCarousel {
  position: relative;
  width: 100%;
}

#castCarousel .carousel-inner {
  padding: 0;
}

#castCarousel .carousel-item {
  padding: 0;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 2rem;
  min-height: 400px;
}

/* Carousel Indicators */
#castCarousel .carousel-indicators {
  margin-bottom: 2rem;
  z-index: 3;
}

/* Carousel Controls */
#castCarousel .carousel-control-prev,
#castCarousel .carousel-control-next {
  width: 5%;
  opacity: 0.5;
  transition: opacity 0.15s ease;
  z-index: 3;
}

#castCarousel .carousel-control-prev:hover,
#castCarousel .carousel-control-next:hover {
  opacity: 0.75;
}

#castCarousel .carousel-control-prev-icon,
#castCarousel .carousel-control-next-icon {
  width: 2rem;
  height: 2rem;
}

.cast-item {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.cast-avatar {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.cast-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cast-no-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cast-info {
  flex: 1;
  min-width: 0;
}

.cast-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.cast-role {
  font-size: 1rem;
  color: #cccccc;
  margin-bottom: 0.5rem;
}

.cast-character {
  font-size: 0.95rem;
  color: #999999;
}

/* 예고편 섹션 */
.trailer-section {
  margin-bottom: 4rem;
}

.trailer-section .section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.video-container {
  position: relative;
  padding-bottom: 45%;
  height: 0;
  overflow: hidden;
  border-radius: 8px;
  background-color: #1a1a1a;
  width: 80%;
  margin: 0 auto;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 리뷰 섹션 */
.reviews-section {
  margin-top: 4rem;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.reviews-section .section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0;
}

.reviews-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-review-create {
  padding: 0.5rem 1.5rem;
  background-color: transparent;
  color: #999999;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-review-create:hover {
  color: #cccccc;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-review-create:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-review-create:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-view-all {
  padding: 0.5rem 1.5rem;
  background-color: transparent;
  color: #999999;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-view-all:hover {
  color: #cccccc;
}

.no-reviews {
  text-align: center;
  padding: 3rem 0;
  color: #cccccc;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.review-card {
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.review-card:hover {
  background-color: #252525;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.review-rating {
  color: #ffc107;
  font-weight: bold;
}

.review-date {
  color: #999999;
  font-size: 0.85rem;
}

.review-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.75rem;
}

.review-content {
  font-size: 0.95rem;
  color: #cccccc;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.review-author {
  font-size: 0.85rem;
  color: #ffffff;
  font-weight: 500;
}

.review-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #999999;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .poster-synopsis-layout {
    flex-direction: column;
  }

  .cast-grid {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 1.5rem;
    min-height: auto;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: 400px;
    padding: 2rem 1rem 6rem 1rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .rating-action-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .cast-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    gap: 1.5rem;
    min-height: auto;
  }

  .main-content-wrapper {
    padding: 2rem 1rem;
  }

  .poster-synopsis-layout {
    flex-direction: column;
    gap: 2rem;
  }

  .cast-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: auto;
    gap: 1.5rem;
  }

  .cast-avatar {
    width: 80px;
    height: 80px;
  }


  .cast-name {
    font-size: 1rem;
  }

  .reviews-grid {
    grid-template-columns: 1fr;
  }
}
</style>