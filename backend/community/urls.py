from django.urls import path
from . import views

urlpatterns = [
    # 리뷰 목록/생성/상세 (ViewSet은 router 써도 되지만, URL 꼬임 방지를 위해 직접 지정 추천)
    path('reviews/', views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:pk>/', views.ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 좋아요
    path('reviews/<int:review_pk>/likes/', views.like_review),

    # 댓글
    path('reviews/<int:review_pk>/comments/', views.comment_list_create),
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_update_delete),
]