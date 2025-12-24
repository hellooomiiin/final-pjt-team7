from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, Comment
from movies.models import Movie

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')  # 닉네임 필드 추가
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'user')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.CharField(source='movie.poster_path', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'movie') # movie는 URL에서 받으므로 read_only 추천