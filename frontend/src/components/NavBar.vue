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
            <router-link class="nav-link btn-login" to="/login">로그인</router-link>
          </li>
          <li v-if="!authStore.isAuthenticated" class="nav-item">
            <router-link class="nav-link btn-register" to="/register">회원가입</router-link>
          </li>
          <li v-if="authStore.isAuthenticated && authStore.user" class="nav-item">
            <router-link class="nav-link btn-profile" to="/profile">
              {{ authStore.user.nickname || authStore.user.email }}님
            </router-link>
          </li>
          <li v-if="authStore.isAuthenticated" class="nav-item">
            <button class="nav-link btn-logout" @click="handleLogout">로그아웃</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const handleLogout = () => {
      authStore.logout()
      router.push('/')
    }

    return {
      authStore,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #ffffff !important;
  border-bottom: 1px solid #000000;
  padding: 1rem 0;
}

/* navbar-dark 클래스가 있어도 검은색 텍스트 유지 */
.navbar-dark .navbar-brand,
.navbar-dark .navbar-brand:hover,
.navbar-dark .navbar-brand:focus,
.navbar-dark .navbar-brand:active {
  color: #000000 !important;
  opacity: 1 !important;
}

.navbar-brand {
  color: #000000 !important;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.navbar-brand:hover,
.navbar-brand:focus,
.navbar-brand:active {
  color: #000000 !important;
  opacity: 1 !important;
}

.navbar-dark .nav-link,
.navbar-dark .nav-link:hover,
.navbar-dark .nav-link:focus,
.navbar-dark .nav-link:active {
  color: #000000 !important;
  opacity: 1 !important;
}

.nav-link {
  color: #000000 !important;
}

.nav-link:hover,
.nav-link:focus,
.nav-link:active {
  color: #000000 !important;
  opacity: 1 !important;
}

.nav-link.router-link-active,
.nav-link.router-link-active:hover,
.nav-link.router-link-active:focus {
  color: #000000 !important;
  opacity: 1 !important;
}

.btn-login {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
}

.btn-login:hover {
  border: 1px solid #000000;
  background-color: #ffffff;
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

.btn-profile {
  border: 1px solid #000000;
  background-color: #ffffff;
  color: #000000;
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  text-decoration: none;
}

.btn-profile:hover {
  background-color: #f0f0f0;
  color: #000000;
}

.btn-logout {
  border: none;
  background-color: transparent;
  color: #000000;
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: inherit;
}

.btn-logout:hover {
  color: #000000;
  text-decoration: underline;
}

/* 햄버거 메뉴 버튼 스타일 */
.navbar-toggler {
  border: 2px solid #000000;
  padding: 0.25rem 0.5rem;
  background-color: transparent;
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25);
  outline: none;
}

/* navbar-dark에서 햄버거 아이콘을 검은색으로 */
.navbar-dark .navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%280, 0, 0, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.navbar-toggler:hover {
  border-color: #000000;
  background-color: #f5f5f5;
}

/* 모바일 메뉴 스타일 개선 */
@media (max-width: 991.98px) {
  .navbar-collapse {
    margin-top: 1rem;
    border-top: 1px solid #e0e0e0;
    padding-top: 1rem;
  }

  .navbar-nav {
    padding: 0;
  }

  .nav-item {
    margin: 0.25rem 0;
  }

  .nav-link {
    padding: 0.75rem 1rem !important;
    border-radius: 4px;
    transition: background-color 0.2s ease;
  }

  .nav-link:hover {
    background-color: #f5f5f5 !important;
  }

  .btn-login,
  .btn-register,
  .btn-profile {
    margin-left: 0 !important;
    margin-top: 0.5rem;
    width: 100%;
    text-align: left;
    display: block;
    border: none !important;
    padding: 0.75rem 1rem !important;
  }

  .btn-logout {
    width: 100%;
    text-align: left;
    padding: 0.75rem 1rem !important;
    border-radius: 4px;
    display: block;
    border: none !important;
    margin-left: 0 !important;
    margin-top: 0.5rem;
  }

  .btn-logout:hover {
    background-color: #f5f5f5 !important;
    text-decoration: none;
  }
}
</style>

