from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from movies.models import Movie

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        # 영화 정보는 URL 파라미터나 request.data에서 가져와야 함 (URL 구조에 따라 다름)
        # 일단은 request.data에 movie ID가 있다고 가정 (프론트 수정 필요 시 설명함)
        serializer.save(user=self.request.user)

    
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