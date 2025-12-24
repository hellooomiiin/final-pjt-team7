from django.db import models
from movies.models import Movie

class MovieMood(models.Model):
    # 1. 영화 ID (1:1 관계)
    # Movie 모델과 연결되며, 영화가 삭제되면 분석 결과도 같이 삭제(CASCADE)됩니다.
    movie = models.OneToOneField(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='mood_result' # movie.mood_result로 접근 가능
    )
    
    # 2. 대표 감정 (가장 점수가 높은 감정 하나)
    # 예: 'sadness', 'realization', 'joy'
    dominant_mood = models.CharField(max_length=50)
    
    # 3. 전체 감정 점수 (AI가 출력한 전체 라벨과 점수)
    # 예: [{'label': 'sadness', 'score': 0.8}, {'label': 'neutral', 'score': 0.1}, ...]
    # JSONField를 사용하면 리스트/딕셔너리 형태를 그대로 DB에 저장할 수 있습니다.
    score_details = models.JSONField(default=list)
    
    # 4. 분석일 (언제 분석했는지 기록)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.dominant_mood}] {self.movie.title}"