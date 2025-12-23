from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'', views.MovieViewSet, basename='movie') # 영화 목록, 상세 조회

urlpatterns = [
    path('popular/', views.MovieViewSet.as_view({'get': 'popular'}), name='movie-popular'),  # GET /movies/popular/ - 인기 영화 목록 (상위 20개)
    path('', include(router.urls)),  # ViewSet의 기본 URL들 포함 (영화 목록, 상세 조회)
]

