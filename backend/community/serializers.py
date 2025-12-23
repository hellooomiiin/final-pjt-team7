from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, Comment

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

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'movie') # movie는 URL에서 받으므로 read_only 추천