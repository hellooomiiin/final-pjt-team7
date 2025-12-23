import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/movies/:id',
    name: 'MovieDetail',
    component: () => import('@/views/MovieDetailView.vue')
  },
  {
    path: '/movies/:id/reviews',
    name: 'MovieReviews',
    component: () => import('@/views/MovieReviewsView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue')
  },
  {
    path: '/profile/edit',
    name: 'ProfileEdit',
    component: () => import('@/views/ProfileEditView.vue')
  },
  {
    path: '/profile/emotions',
    name: 'ProfileEmotions',
    component: () => import('@/views/ProfileEmotionsView.vue')
  },
  {
    path: '/profile/reviews',
    name: 'ProfileReviews',
    component: () => import('@/views/ProfileReviewsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

