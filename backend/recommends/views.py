import random 
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Recommendation
from .serializers import RecommendationSerializer
from movies.models import Movie
from movies.serializers import MovieListSerializer

MOOD_MAPPING = {
    # 1. 심심할 땐 -> 자극적인 것 (흥미, 놀람, 깨달음/반전, 공포)
    'bored': ['excitement', 'curiosity', 'surprise', 'realization', 'fear'],
    
    # 2. 화날 땐 -> 다 때려부수는 것 (분노) 혹은 통쾌함 (흥미)
    'angry': ['anger', 'annoyance', 'excitement'],
    
    # 3. 슬플 땐 -> 같이 울어줄 영화 (슬픔, 후회)
    'sad': ['sadness', 'grief', 'remorse', 'disappointment'],
    
    # 4. 행복할 땐 -> 계속 행복하게 (기쁨, 즐거움, 사랑, 존경)
    'happy': ['joy', 'amusement', 'love', 'admiration', 'optimism'],
    
    # 5. 긴장/스트레스 -> 편안하고 따뜻한 것 (안도감, 승인)
    'stressed': ['relief', 'approval', 'caring', 'joy']
}

# 1. 추천 생성 및 저장 (POST)
# 로그인한 유저만 저장할 수 있도록 설정 (선택사항)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def generate_recommendation(request):
    # 프론트에서 보낸 기분 데이터 받기 ({ "mood": "sad" })
    user_mood = request.data.get('mood')
    target_moods = MOOD_MAPPING.get(user_mood, [])
    
    recommended_movies = []
    
    if target_moods:
        # 1. 감정에 맞는 영화 필터링
        candidates = Movie.objects.filter(
            mood_result__dominant_mood__in=target_moods
        )
        
        # 2. [핵심] 인기도 순으로 정렬 후 상위 30개 가져오기 (후보군)
        # 평점도 중요하다면: .order_by('-popularity', '-vote_average')
        top_candidates = candidates.order_by('-popularity')[:30]
        
        # QuerySet을 리스트로 변환 (random.sample을 쓰기 위해)
        top_candidates_list = list(top_candidates)
        
        # 3. [핵심] 상위 30개 중에서 랜덤으로 4개 뽑기
        if len(top_candidates_list) >= 4:
            recommended_movies = random.sample(top_candidates_list, 4)
        else:
            # 만약 후보가 4개보다 적으면 있는 거 다 보여줌
            recommended_movies = top_candidates_list
            
    else:
        # 매핑 안 된 기분일 때도 인기도 기반 랜덤 추천
        top_candidates = Movie.objects.order_by('-popularity')[:30]
        recommended_movies = random.sample(list(top_candidates), 4)

    # 4. DB에 기록 저장 (기존 로직 동일)
    # 선택된 영화들(recommended_movies)은 리스트이므로 바로 set() 가능
    if request.user.is_authenticated:
        recommendation = Recommendation.objects.create(
            user=request.user,
            mood=user_mood
        )
        recommendation.recommended_movies.set(recommended_movies)

    # 5. 응답
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