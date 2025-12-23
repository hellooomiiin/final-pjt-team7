from rest_framework import serializers
from .models import (
    Movie, Genre, Person, MovieCast, MovieCrew,
    MovieKeyword, MovieImage, MovieVideo, UserMovieWishlist
)
from community.serializers import ReviewSerializer
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'tmdb_id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'tmdb_id', 'name', 'profile_path', 'biography', 'birthday', 'place_of_birth')


class MovieCastSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = MovieCast
        fields = ('person', 'character', 'order')


class MovieCrewSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = MovieCrew
        fields = ('person', 'job', 'department')


class MovieKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieKeyword
        fields = ('id', 'tmdb_id', 'name')


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ('file_path', 'aspect_ratio', 'height', 'width', 'vote_average', 'vote_count')


class MovieVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('key', 'name', 'site', 'type', 'official')


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'tmdb_id', 'title', 'original_title', 'overview',
            'release_date', 'poster_path', 'backdrop_path', 'vote_average',
            'vote_count', 'popularity', 'genres', 'runtime'
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    cast = MovieCastSerializer(many=True, read_only=True)
    crew = MovieCrewSerializer(many=True, read_only=True)
    keywords = MovieKeywordSerializer(many=True, read_only=True)
    images = MovieImageSerializer(many=True, read_only=True)
    videos = MovieVideoSerializer(many=True, read_only=True)
    is_wishlisted = serializers.SerializerMethodField()
    review_set = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'tmdb_id', 'title', 'original_title', 'overview',
            'release_date', 'poster_path', 'backdrop_path', 'vote_average',
            'vote_count', 'popularity', 'genres', 'runtime', 'tagline',
            'cast', 'crew', 'keywords', 'images', 'videos', 'is_wishlisted',
            'created_at', 'updated_at', 'review_set'
        )

    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserMovieWishlist.objects.filter(user=request.user, movie=obj).exists()
        return False
    