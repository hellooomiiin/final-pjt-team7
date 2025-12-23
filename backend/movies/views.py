from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MovieListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve': # 상세 조회 (GET /movies/1/)
            return MovieDetailSerializer
        return MovieListSerializer    # 나머지 (목록 조회 등)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """인기 영화 목록"""
        movies = Movie.objects.all().order_by('-popularity')[:20]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)