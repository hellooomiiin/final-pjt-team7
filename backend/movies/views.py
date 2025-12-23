from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

# 1. Home 페이지: 인기 영화 Top 20 조회
@api_view(['GET'])
def movie_popular(request):
    # popularity 필드 기준 내림차순 정렬 후 20개 슬라이싱
    movies = Movie.objects.order_by('-popularity')[:20]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 2. 특정 영화 1개 상세 조회 (movie_id로 요청)
@api_view(['GET'])
def movie_detail(request, movie_pk):
    # tmdb_id를 기준으로 조회 (DB에 없으면 404 에러)
    movie = get_object_or_404(Movie, tmdb_id=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

# 3. 여러 영화 ID로 정보 조회 (장바구니, 좋아요 목록 등)
# 요청 예시: GET /movies/list/?ids=101,102,103
@api_view(['GET'])
def movie_list_by_ids(request):
    ids = request.GET.get('ids', '') # URL 쿼리 파라미터에서 ids 가져오기
    
    if not ids:
        return Response({'error': 'ids parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 콤마로 분리하여 리스트로 변환
    id_list = [int(id) for id in ids.split(',') if id.isdigit()]
    
    # tmdb_id가 id_list 안에 있는 영화들 필터링
    movies = Movie.objects.filter(tmdb_id__in=id_list)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)
