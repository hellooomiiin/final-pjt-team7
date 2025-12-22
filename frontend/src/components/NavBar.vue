<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <span class="film-icon">🎬</span>
        <span class="ms-2">Mood-Match</span>
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">홈</router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li v-if="!authStore.isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/login">로그인</router-link>
          </li>
          <li v-if="!authStore.isAuthenticated" class="nav-item">
            <router-link class="nav-link btn-register" to="/register">회원가입</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  border-bottom: 1px solid #000000;
  padding: 1rem 0;
}

.navbar-brand {
  color: #000000;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-link {
  color: #000000;
}

.nav-link:hover {
  color: #000000;
}

.btn-register {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
}

.btn-register:hover {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
}
</style>

