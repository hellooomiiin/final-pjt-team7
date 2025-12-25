<template>
  <div class="search-container">
    <div class="container">
      <h2 class="page-title">
        "{{ searchQuery }}" 검색 결과
      </h2>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-danger" role="status"></div>
      </div>

      <div v-else-if="movies.length === 0" class="empty-state">
        <p>검색 결과가 없습니다. 😢</p>
        <small>다른 키워드로 검색해 보세요.</small>
      </div>

      <div v-else class="movies-grid">
        <div 
          v-for="movie in movies" 
          :key="movie.tmdb_id" 
          class="movie-card"
          @click="$router.push(`/movies/${movie.tmdb_id}`)"
        >
          <img :src="getImageUrl(movie.poster_path)" class="movie-poster" />
          <div class="movie-info">
            <h5 class="movie-title">{{ movie.title }}</h5>
            <span class="movie-year">{{ movie.release_date?.split('-')[0] }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'SearchView',
  setup() {
    const route = useRoute()
    const movies = ref([])
    const loading = ref(false)
    const searchQuery = ref('')

    const fetchMovies = async (query) => {
      if (!query) return
      loading.value = true
      searchQuery.value = query
      
      try {
        // Django API 호출
        const res = await axios.get('http://127.0.0.1:8000/api/v1/movies/', {
          params: { search: query }
        })
        movies.value = res.data
      } catch (err) {
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const getImageUrl = (path) => {
      return path ? `https://image.tmdb.org/t/p/w500${path}` : '/assets/no-poster.png'
    }

    // 1. 페이지 처음 들어왔을 때 실행
    onMounted(() => {
      fetchMovies(route.query.q)
    })

    // 2. 검색어가 바뀌면(URL이 바뀌면) 다시 실행 (중요!)
    watch(() => route.query.q, (newQuery) => {
      fetchMovies(newQuery)
    })

    return { movies, loading, searchQuery, getImageUrl }
  }
}
</script>

<style scoped>
.search-container { padding: 3rem 0; min-height: 80vh; }
.page-title { margin-bottom: 2rem; font-weight: bold; }
.empty-state { text-align: center; padding: 5rem 0; color: #666; }

/* 그리드 레이아웃 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}
.movie-card { cursor: pointer; transition: transform 0.2s; }
.movie-card:hover { transform: translateY(-5px); }
.movie-poster { width: 100%; aspect-ratio: 2/3; object-fit: cover; border-radius: 8px; margin-bottom: 0.5rem; }
.movie-title { font-size: 1.1rem; font-weight: bold; margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }
.movie-year { color: #666; font-size: 0.9rem; }
</style>