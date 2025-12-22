from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Movie
from .serializers import MovieListSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MovieListSerializer

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """인기 영화 목록"""
        movies = Movie.objects.all().order_by('-popularity')[:20]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

