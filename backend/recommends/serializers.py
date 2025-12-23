from rest_framework import serializers
from .models import Recommendation
from movies.serializers import MovieListSerializer # 기존에 만들어둔 영화 목록용 시리얼라이저

class RecommendationSerializer(serializers.ModelSerializer):
    # 역참조된 영화들의 상세 정보를 포함해서 보여주기 위해 nesting
    recommended_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'mood', 'recommended_movies', 'created_at']
        read_only_fields = ('user', 'recommended_movies', 'created_at')