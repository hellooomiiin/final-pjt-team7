<template>
  <div class="movie-detail-container">
    <div class="container py-5">
      <div v-if="loading" class="text-center loading-spinner py-5">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="movie" class="movie-detail">
        <div class="row">
          <div class="col-md-4 mb-4">
            <img
              :src="getImageUrl(movie.poster_path, 'poster')"
              class="movie-poster-large img-fluid rounded shadow"
              :alt="movie.title"
            />
          </div>
          
          <div class="col-md-8">
            <h1 class="movie-title fw-bold">{{ movie.title }}</h1>
            <p v-if="movie.original_title" class="movie-original-title text-muted fs-5">
              {{ movie.original_title }}
            </p>
            
            <div class="movie-info mt-4">
              <p v-if="movie.overview" class="movie-overview lead">{{ movie.overview }}</p>
              
              <div class="movie-meta d-flex flex-wrap gap-3 my-3">
                <span v-if="movie.release_date" class="badge bg-dark px-3 py-2">
                  개봉일: {{ movie.release_date }}
                </span>
                <span v-if="movie.runtime" class="badge bg-dark px-3 py-2">
                  상영시간: {{ movie.runtime }}분
                </span>
                <span v-if="movie.vote_average" class="badge bg-warning text-dark px-3 py-2">
                  평점: ★ {{ movie.vote_average.toFixed(1) }}
                </span>
                <span v-if="movie.popularity" class="badge bg-info text-dark px-3 py-2">
                  인기도: {{ movie.popularity.toFixed(0) }}
                </span>
              </div>

              <div class="people-info mt-4 p-3 bg-light rounded">
                <div v-if="movie.director" class="mb-3">
                  <span class="fw-bold">감독:</span> <span class="ms-2 text-primary">{{ movie.director }}</span>
                </div>

                <div v-if="movie.actors && movie.actors.length" class="actors-list">
                  <p class="fw-bold mb-2">출연진</p>
                  <div class="d-flex flex-wrap gap-3 mt-2">
                    <div v-for="actor in movie.actors.slice(0, 5)" :key="actor.name" class="actor-card text-center" style="width: 80px;">
                      <img 
                        :src="getImageUrl(actor.profile_path, 'actor')" 
                        class="actor-img rounded-circle mb-1" 
                        style="width: 60px; height: 60px; object-fit: cover;"
                        alt="actor"
                      >
                      <div class="actor-name small fw-bold text-truncate">{{ actor.name }}</div>
                      <div class="actor-char text-muted text-truncate" style="font-size: 0.7rem;">{{ actor.character }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="movie.genres && movie.genres.length" class="mt-4">
                <span v-for="genre in movie.genres" :key="genre.tmdb_id" class="badge rounded-pill bg-secondary me-2 px-3">
                  #{{ genre.name }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="trailerVideoId" class="trailer-section mt-5">
          <h3 class="section-title mb-3">공식 예고편</h3>
          <div class="ratio ratio-16x9 shadow rounded overflow-hidden">
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
            <router-link 
              :to="{ name: 'movie-reviews', params: { id: movie.id } }" 
              class="btn btn-sm btn-outline-dark"
            >
              전체보기 &rarr;
            </router-link>
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
                @click="$router.push({ name: 'review-detail', params: { id: movie.id, reviewId: review.id } })"
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
                    <span class="small fw-bold">by {{ review.user }}</span>
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
      </div> <div v-else class="alert alert-warning text-center">
        영화 정보를 찾을 수 없습니다.
      </div>
    </div>
  </div>
</template>

<style scoped>
.hover-effect {
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
.movie-poster-large {
  max-height: 500px;
  width: 100%;
  object-fit: cover;
}
</style>