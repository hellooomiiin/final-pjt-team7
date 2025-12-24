from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from movies.models import Movie

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        """
        리뷰 목록 조회 시 movie 필터 지원
        """
        queryset = Review.objects.all()
        movie_id = self.request.query_params.get('movie', None)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset
    
    # 영화 정보는 URL 파라미터나 request.data에서 가져와야 함 (URL 구조에 따라 다름)
    def perform_create(self, serializer):
        # request.data에서 movie ID 가져오기
        movie_id = self.request.data.get('movie')
        if not movie_id:
            raise ValidationError({'movie': '영화 ID가 필요합니다.'})
        
        # Movie 객체 가져오기
        movie = get_object_or_404(Movie, pk=movie_id)
        
        # user와 movie를 함께 저장
        # 중복 체크는 프론트엔드에서 처리하고, 데이터베이스 레벨의 unique_together 제약 조건으로도 보호됨
        serializer.save(user=self.request.user, movie=movie)

    
# ★ 좋아요 기능 (POST 요청)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user) # 좋아요 취소
        liked = False
    else:
        review.like_users.add(request.user)    # 좋아요
        liked = True
    return Response({'liked': liked, 'count': review.like_users.count()})
    

# ★ [추가] CommentViewSet: 댓글 CRUD
@api_view(['GET', 'POST'])
def comment_list_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_update_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 본인 댓글인지 확인
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        comment.delete()
        return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 로그인한 유저만 접근 가능
def user_reviews(request):
    # request.user: 토큰을 통해 확인된 현재 접속 유저
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)