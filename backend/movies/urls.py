from django.urls import path
from . import views

urlpatterns = [
    path('popular/', views.movie_popular, name='movie_popular'), # GET /movies/popular/
    path('list/', views.movie_list_by_ids, name='movie_list_by_ids'), # GET /movies/list/?ids=1,2,3
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'), # GET /movies/12345/
]