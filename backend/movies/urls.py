from django.urls import path
from . import views

urlpatterns = [
    path('popular/', views.movie_popular, name='movie_popular'), # GET /movies/popular/
    path('list/', views.movie_list_by_ids, name='movie_list_by_ids'), # GET /movies/list/?ids=1,2,3
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'), # GET /movies/12345/
    # 찜하기 (POST): /api/v1/movies/123/likes/
    path('<int:movie_pk>/likes/', views.likes, name='likes'),
    # 내가 찜한 목록 (GET): /api/v1/movies/my-likes/
    path('my-likes/', views.my_like_movies, name='my_like_movies'),
    
    path('', views.movie_list, name='movie_list'),
]