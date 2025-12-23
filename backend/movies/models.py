from django.db import models

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
    poster_path = models.CharField(max_length=200, blank=True, null=True) # 이미지 URL 뒷부분
    release_date = models.DateField(blank=True, null=True)
    
    # 인기순 정렬을 위해 필요 (Home 화면 요청 대응)
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    
    runtime = models.IntegerField(null=True, blank=True) # 분 단위
    director = models.CharField(max_length=100, null=True, blank=True) # 감독 이름
    
    # 배우 데이터는 [{name: 'Tom', profile_path: '/abc.jpg'}, ...] 형태의 리스트로 저장
    # SQLite/PostgreSQL 모두 지원 (Django 3.1+)
    actors = models.JSONField(default=list, null=True, blank=True)

    # 장르와의 관계 (Many-to-Many)
    # DB에는 'movies_movie_genres' 라는 테이블이 자동으로 생성되어 매칭 정보를 관리합니다.
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title