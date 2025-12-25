from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

@api_view(['GET'])
def movie_list(request):
    search_keyword = request.GET.get('search', '').strip()
    
    if search_keyword:
        # 제목이나 원제에 검색어가 포함된 영화 검색
        movies = Movie.objects.filter(
            Q(title__icontains=search_keyword)
        ).order_by('-popularity') # 인기도순 정렬
    else:
        # 검색어 없으면 빈 리스트 반환 (혹은 전체 목록)
        movies = [] 

    # 검색 결과 페이지이므로 개수 제한 없이(또는 넉넉하게) 보냅니다.
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

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


# 찜하기 기능 (토글)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # 이미 찜한 상태면 -> 취소 (remove)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        is_liked = False
    # 찜하지 않은 상태면 -> 추가 (add)
    else:
        movie.like_users.add(request.user)
        is_liked = True
        
    context = {
        'is_liked': is_liked,
        'count': movie.like_users.count() # 현재 찜한 사람 수도 같이 반환하면 좋음
    }
    return Response(context, status=status.HTTP_200_OK)


# 내가 찜한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_like_movies(request):
    # 역참조(related_name)를 이용해 내가 찜한 영화들을 가져옴
    movies = request.user.like_movies.all().order_by('-pk') # 최신순 정렬
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)