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

				<div class="reviews-section mt-5 pt-4 border-top">
					<div class="d-flex justify-content-between align-items-center mb-4">
						<h3 class="section-title mb-0">리뷰 ({{ movie.review_set ? movie.review_set.length : 0 }})</h3>
						<div class="d-flex gap-2 align-items-center">
							<!-- 로그인 상태일 때만 리뷰 작성하기 버튼 표시 -->
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
										<small class="text-muted">{{ new Date(review.created_at).toLocaleDateString() }}</small>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // 인증 스토어 import

export default {
  name: 'MovieDetailView',
  setup() {
    // 1. 기본 변수 및 도구 설정
    const route = useRoute()   // 현재 URL 정보 가져오기용
    const router = useRouter() // 페이지 이동용 (router.push)
    const authStore = useAuthStore() // 인증 스토어 인스턴스 생성
    
    const movie = ref(null)
    const loading = ref(true)  // 로딩 상태 (템플릿 v-if="loading"을 위해 필수)
    const trailerVideoId = ref(null)


    // 2. 헬퍼 함수들 (템플릿을 깔끔하게 만들기 위함)

    // [날짜 포맷팅] 예: 2023-12-25T... -> 2023년 12월 25일
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // [페이지 이동] 리뷰 상세 페이지로 이동
    const goReviewDetail = (reviewId) => {
      if (!movie.value) return
      
      router.push({ 
        name: 'review-detail', 
        params: { 
          id: movie.value.tmdb_id, // 영화 ID (tmdb_id 사용)
          reviewId: reviewId  // 리뷰 ID
        } 
      })
    }

    // [페이지 이동] 리뷰 작성 페이지로 이동 (이미 리뷰 작성 여부 확인)
    const goReviewCreate = async () => {
      if (!movie.value) return
      
      try {
        // authStore.user가 없으면 fetchProfile로 최신 정보 가져오기
        if (!authStore.user) {
          await authStore.fetchProfile()
        }
        
        // movie.value.id는 DB의 id (Movie 모델의 PK)
        // Review 모델의 movie 필드는 Movie의 id를 참조하므로 movie.value.id 사용
        // API를 직접 호출해서 현재 사용자가 이미 이 영화에 리뷰를 작성했는지 확인
        const response = await axios({
          method: 'get',
          url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
          params: {
            movie: movie.value.id
          },
          headers: { Authorization: `Bearer ${authStore.token}` }
        })
        
        const currentUsername = authStore.user?.username
        
        // 페이지네이션된 응답이므로 response.data.results 사용
        const reviews = response.data.results || response.data
        
        // 응답에서 현재 사용자가 작성한 리뷰가 있는지 확인
        const hasMyReview = Array.isArray(reviews) && reviews.some(
          review => review.user === currentUsername
        )
        
        if (hasMyReview) {
          alert('이미 이 영화에 리뷰를 작성하셨습니다.')
          return // 페이지 이동하지 않음
        }
      } catch (error) {
        // API 호출 실패 시에도 작성 페이지로 이동 (에러 무시)
        console.error('리뷰 확인 중 오류:', error)
      }
      
      // 리뷰가 없거나 현재 사용자가 작성한 리뷰가 없으면 작성 페이지로 이동
      // 백엔드 영화 API는 tmdb_id를 기대하므로 tmdb_id 전달
      router.push({ 
        name: 'review-create', 
        params: { 
          id: movie.value.tmdb_id // tmdb_id 전달
        } 
      })
    }

    // [이미지 경로 생성] 포스터/배우 사진 구분
    const getImageUrl = (path, type = 'poster') => {
      // 이미지가 없을 때 대체 이미지 처리
      if (!path) {
        return type === 'actor' ? '/assets/no-profile.png' : '/assets/no-poster.png'
      }
      
      // 이미지 사이즈 최적화 (배우는 작게, 포스터는 크게)
      const size = type === 'actor' ? 'w185' : 'w500'
      return `https://image.tmdb.org/t/p/${size}${path}`
    }

    // 3. API 호출 함수들

    // [유튜브] 예고편 검색
    const fetchTrailer = async (query) => {
			
			// .env 파일에서 키 가져오기
			const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
			console.log(YOUTUBE_API_KEY)
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

    // [Django] 영화 상세 정보 가져오기
    const fetchMovieDetail = async () => {
      loading.value = true
      try {
        const movieId = route.params.id
        // 백엔드 주소 (api/v1/movies/...)
        const movieResponse = await axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/`)
        movie.value = movieResponse.data
        
        // 영화 정보 로드 성공 시 -> 리뷰 목록과 예고편 검색
        if (movie.value) {
          // 리뷰 목록 가져오기 (review_set이 없을 수 있으므로 별도로 호출)
          // 토큰 없이도 조회 가능하므로 헤더 제거
          try {
            const reviewsResponse = await axios({
              method: 'get',
              url: `http://127.0.0.1:8000/api/v1/community/reviews/`,
              params: {
                movie: movie.value.id // DB의 id 사용
              }
            })
            
            // review_set이 없으면 리뷰 목록 API에서 가져온 데이터로 추가
            if (!movie.value.review_set) {
              movie.value.review_set = reviewsResponse.data.results || reviewsResponse.data
            }
          } catch (reviewError) {
            console.error('리뷰 목록 로드 실패:', reviewError)
            // 리뷰 목록 로드 실패해도 영화 정보는 표시
            if (!movie.value.review_set) {
              movie.value.review_set = []
            }
          }
          
          // 예고편 검색 시작
          await fetchTrailer(movie.value.title)
        }
      } catch (error) {
        console.error('영화 상세 정보 로드 실패:', error)
      } finally {
        loading.value = false
      }
    }

    // 4. 라이프사이클 (화면 켜질 때 실행)
    onMounted(() => {
      fetchMovieDetail()
    })

    // 5. 템플릿(HTML)으로 변수/함수 내보내기
    return {
      movie,
      loading,
      trailerVideoId,
      authStore,       // 인증 스토어 (로그인 상태 확인용)
      getImageUrl,
      formatDate,      // 템플릿에서 사용하기 위해 반환
      goReviewDetail,  // 템플릿에서 사용하기 위해 반환
      goReviewCreate   // 리뷰 작성 페이지로 이동하는 함수
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

/* 리뷰 작성하기 버튼 스타일 - 전체보기 버튼과 동일하되 테두리 없음 + 호버 효과 */
.btn-review-create {
	border: none !important;
	outline: none !important;
	box-shadow: none !important;
	color: #000000;
	transition: opacity 0.2s ease;
}

.btn-review-create:hover {
	opacity: 0.7;
}

.btn-review-create:focus {
	outline: none !important;
	box-shadow: none !important;
}

/* 모바일 대응 */
@media (max-width: 768px) {
	.movie-title { font-size: 1.8rem; }
	.movie-poster-large { margin-bottom: 2rem; }
}
</style>