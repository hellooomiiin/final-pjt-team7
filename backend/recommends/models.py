from django.db import models
from django.conf import settings
from movies.models import Movie 

class Recommendation(models.Model):
    # 1. 추천받은 유저 (User 모델과 1:N 관계)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='recommendations'
    )
    
    # 2. 입력했던 기분/상황 (나중에 필터링할 때 유용)
    mood = models.CharField(max_length=50) 
    
    # 3. 추천된 영화 목록 (영화 모델과 N:M 관계)
    # 하나의 기록에 여러 영화가 포함되므로 ManyToManyField 사용
    recommended_movies = models.ManyToManyField(
        Movie, 
        related_name='recommended_records'
    )
    
    # 4. 추천받은 날짜
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}님의 추천 기록 - {self.created_at}"