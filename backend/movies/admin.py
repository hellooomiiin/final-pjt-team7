from django.contrib import admin
from .models import (
    Movie, Genre, Person, MovieCast, MovieCrew,
    MovieKeyword, MovieImage, MovieVideo, UserMovieWishlist
)

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(MovieCast)
admin.site.register(MovieCrew)
admin.site.register(MovieKeyword)
admin.site.register(MovieImage)
admin.site.register(MovieVideo)
admin.site.register(UserMovieWishlist)

