from django.urls import path
from . import views

urlpatterns = [
    # 1. 추천 생성: POST /api/v1/recommends/generate/
    path('generate/', views.generate_recommendation, name='generate_recommendation'),
    
    # 2. 기록 조회: GET /api/v1/recommends/history/
    path('history/', views.recommendation_history, name='recommendation_history'),
]