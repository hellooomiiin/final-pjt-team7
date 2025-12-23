import { createRouter, createWebHistory } from 'vue-router'
import RecommendView from '@/views/RecommendView.vue'


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
    path: '/recommend',
    name: 'recommend',
    component: () => import('@/views/RecommendView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

