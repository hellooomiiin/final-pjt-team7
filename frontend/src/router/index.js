import { createRouter, createWebHistory } from 'vue-router'
import ReviewDetailView from '@/views/ReviewDetailView.vue'
import MovieReviewsView from '@/views/MovieReviewsView.vue'
import ReviewCreateView from '@/views/ReviewCreateView.vue'
import ReviewUpdateView from '@/views/ReviewUpdateView.vue'
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
    // 주소 모양: /movies/1/reviews/5 (영화 1번의 리뷰 5번)
    path: '/movies/:id/reviews/:reviewId', 
    name: 'review-detail',
    component: ReviewDetailView
    },
  {
    path: '/movies/:id/reviews',
    name: 'movie-reviews', // 이 이름을 기억하세요!
    component: MovieReviewsView
  },
  {
    path: '/movies/:id/reviews/create', // 주소 모양: /movies/1/reviews/create
    name: 'review-create',
    component: ReviewCreateView
  },
  {
  path: '/movies/:id/reviews/:reviewId/update',
  name: 'review-update',
  component: ReviewUpdateView
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
  },
  {
    path: '/profile/dibs',
    name: 'ProfileDibs',
    component: () => import('@/views/ProfileDibsView.vue')
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

