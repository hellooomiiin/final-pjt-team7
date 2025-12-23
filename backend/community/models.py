from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.
class Review(models.Model):
    # 누가 썼는지 (User 연결)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 어떤 영화인지 (Movie 연결)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100) # 제목
    content = models.TextField()             # 내용
    rank = models.IntegerField(default=5)    # 평점 (아까 프론트에서 rank 보냈죠?)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)
    
    class Meta:
        # 한 유저는 한 영화에 하나의 리뷰만 작성 가능
        unique_together = [['user', 'movie']]

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments') # 어떤 리뷰의 댓글인지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)      # 누가 썼는지
    content = models.TextField()                                                      # 내용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)