from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Recommendation
from .serializers import RecommendationSerializer
from movies.models import Movie
from movies.serializers import MovieListSerializer

# 1. 추천 생성 및 저장 (POST)
# 로그인한 유저만 저장할 수 있도록 설정 (선택사항)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def generate_recommendation(request):
    # 프론트에서 보낸 기분 데이터 받기 ({ "mood": "sad" })
    mood = request.data.get('mood')
    
    # --- [AI 로직 대체 부분] ---
    # 현재는 랜덤으로 4개를 뽑지만, 나중에 여기에 AI 알고리즘을 넣는다.
    # 예: "sad"면 장르가 드라마인 것 중에서 뽑기 등
    recommended_movies = Movie.objects.order_by('?')[:4]
    # -------------------------

    # DB에 기록 저장
    recommendation = Recommendation.objects.create(
        user=request.user,
        mood=mood
    )
    # ManyToMany 필드에 영화 목록 추가
    recommendation.recommended_movies.set(recommended_movies)

    # 응답은 "방금 추천된 영화 목록"만 보내주면 됨 (RecommendView에서 바로 보여줄 것)
    serializer = MovieListSerializer(recommended_movies, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# 2. 내 추천 기록 조회 (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_history(request):
    # 내가 받은 추천 기록만 가져오기 (최신순)
    histories = Recommendation.objects.filter(user=request.user)
    
    serializer = RecommendationSerializer(histories, many=True)
    return Response(serializer.data)