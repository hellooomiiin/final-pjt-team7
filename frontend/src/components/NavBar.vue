<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid navbar-container">
      <router-link class="navbar-brand" to="/">
        <div class="logo-wrapper">
          <svg
            class="logo-svg"
            viewBox="0 0 600 150"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <path id="curve" d="M 50 130 Q 300 70 550 130" />
            </defs>
            <text>
              <textPath href="#curve" startOffset="50%" text-anchor="middle">
                Mood-Match
              </textPath>
            </text>
          </svg>
        </div>
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
            <router-link class="nav-link home-link" to="/">홈</router-link>
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
@font-face {
  font-family: 'Tmon';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/TmonMonsori.woff') format('woff');
  font-weight: normal;
  font-display: swap;
}

.navbar {
  background-color: #000000 !important;
  border-bottom: none !important;
  padding: 1rem 0;
}

.navbar-container {
  max-width: 1330px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* navbar-dark 클래스 - 로고는 별도 스타일 적용 */
.navbar-dark .navbar-brand,
.navbar-dark .navbar-brand:hover,
.navbar-dark .navbar-brand:focus,
.navbar-dark .navbar-brand:active {
  opacity: 1 !important;
}

.navbar-brand {
  text-decoration: none;
  padding: 0;
}

.logo-wrapper {
  display: flex;
  align-items: center;
}

.logo-svg {
  width: 100%;
  max-width: 175px;
  height: auto;
}

.logo-svg text {
  fill: #E50914; /* primary40 색상 */
  font-size: 63px;
  font-weight: normal;
  font-family: 'Tmon', sans-serif;
}

.navbar-dark .nav-link,
.navbar-dark .nav-link:hover,
.navbar-dark .nav-link:focus,
.navbar-dark .nav-link:active {
  opacity: 1 !important;
}

.nav-link {
  color: #808080 !important; /* 회색 */
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 0.5rem 1rem;
}

.nav-link:hover,
.nav-link:focus,
.nav-link:active {
  background-color: rgba(0, 0, 0, 0.8) !important; /* 어두운 배경 */
  color: #ffffff !important; /* 흰색 텍스트 */
  opacity: 1 !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.nav-link.router-link-active,
.nav-link.router-link-active:hover,
.nav-link.router-link-active:focus {
  color: #ffffff !important; /* 현재 페이지는 흰색 */
  opacity: 1 !important;
}

.home-link {
  padding-bottom: 4px !important;
}

.btn-login {
  border: none;
  background-color: transparent;
  color: #808080; /* 회색 텍스트 */
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-login:hover {
  background-color: rgba(0, 0, 0, 0.8); /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border-radius: 8px;
}

.btn-register {
  border: none;
  background-color: transparent;
  color: #808080; /* 회색 텍스트 */
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-register:hover {
  background-color: rgba(0, 0, 0, 0.8); /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border-radius: 8px;
}

.btn-profile {
  border: none;
  background-color: transparent;
  color: #808080; /* 회색 텍스트 */
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-profile:hover {
  background-color: rgba(0, 0, 0, 0.8); /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border-radius: 8px;
}

.btn-logout {
  border: none !important;
  background-color: transparent;
  color: #808080; /* 회색 텍스트 */
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: inherit;
  text-decoration: none;
  outline: none !important;
  box-shadow: none !important;
}

.btn-logout:hover {
  background-color: rgba(0, 0, 0, 0.8); /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border-radius: 8px;
  text-decoration: none;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn-logout:focus,
.btn-logout:active {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

/* 햄버거 메뉴 버튼 스타일 */
.navbar-toggler {
  border: 2px solid #ffffff;
  padding: 0.25rem 0.5rem;
  background-color: transparent;
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
  outline: none;
}

/* navbar-dark에서 햄버거 아이콘을 흰색으로 */
.navbar-dark .navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.navbar-toggler:hover {
  border-color: #ffffff;
  background-color: rgba(255, 255, 255, 0.1);
}

/* 모바일 메뉴 스타일 개선 - 다크 테마 */
@media (max-width: 991.98px) {
  .navbar-collapse {
    margin-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
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
    border-radius: 8px;
    transition: all 0.3s ease;
  }

  .nav-link:hover {
    background-color: rgba(0, 0, 0, 0.8) !important;
    color: #ffffff !important;
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
    border-radius: 8px;
    display: block;
    border: none !important;
    margin-left: 0 !important;
    margin-top: 0.5rem;
  }

  .btn-logout:hover {
    background-color: rgba(0, 0, 0, 0.8) !important;
    color: #ffffff !important;
    text-decoration: none;
  }
}
</style>

