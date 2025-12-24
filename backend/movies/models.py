from django.db import models
from django.conf import settings

class Genre(models.Model):
    # TMDb에서 제공하는 장르 ID (예: 28, 12)를 그대로 저장
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    # TMDb 영화 ID (PK 역할, 중복 방지)
    tmdb_id = models.IntegerField(unique=True)
    
    # 기본 정보
    title = models.CharField(max_length=200)
    overview = models.TextField(blank=True, null=True)
    overview_en = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=200, blank=True, null=True) # 이미지 URL 뒷부분
    release_date = models.DateField(blank=True, null=True)
    
    # 인기순 정렬을 위해 필요 (Home 화면 요청 대응)
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    
    runtime = models.IntegerField(null=True, blank=True) # 분 단위
    director = models.CharField(max_length=100, null=True, blank=True) # 감독 이름
    
    # 배우 데이터는 [{name: 'Tom', profile_path: '/abc.jpg'}, ...] 형태의 리스트로 저장
    actors = models.JSONField(default=list, null=True, blank=True)

    # 장르와의 관계 (Many-to-Many)
    # DB에는 'movies_movie_genres' 라는 테이블이 자동으로 생성되어 매칭 정보를 관리합니다.
    genres = models.ManyToManyField(Genre, related_name='movies')
    
    # 찜한 유저들 (M:N 관계)
    # related_name='like_movies'로 설정하면, 
    # 나중에 유저 입장에서 user.like_movies.all()로 내가 찜한 영화를 찾을 수 있음
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='like_movies', 
        blank=True
    )

    def __str__(self):
        return self.title
