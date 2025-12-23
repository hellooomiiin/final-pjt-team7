from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['tmdb_id', 'name']

class MovieListSerializer(serializers.ModelSerializer):
    # 목록(Home)에서는 줄거리(overview) 등 무거운 정보는 뺍니다.
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'poster_path', 'vote_average', 'release_date']

class MovieDetailSerializer(serializers.ModelSerializer):
    # 상세 페이지용: 장르 정보 포함, 줄거리 포함
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__' # 모든 필드 포함