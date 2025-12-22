from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.URLField(null=True, blank=True)
    backdrop_path = models.URLField(null=True, blank=True)
    vote_average = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True, blank=True
    )
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre, related_name='movies')
    runtime = models.IntegerField(null=True, blank=True)
    tagline = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-popularity']

    def __str__(self):
        return self.title


class Person(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    profile_path = models.URLField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['movie', 'person', 'order']


class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='crew')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    job = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ['movie', 'person', 'job']


class MovieKeyword(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='keywords')

    def __str__(self):
        return self.name


class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    file_path = models.URLField()
    aspect_ratio = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-vote_average']


class MovieVideo(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')
    key = models.CharField(max_length=100)  # YouTube video ID
    name = models.CharField(max_length=200)
    site = models.CharField(max_length=50, default='YouTube')
    type = models.CharField(max_length=50)  # Trailer, Teaser, etc.
    official = models.BooleanField(default=False)

    class Meta:
        ordering = ['-official', 'type']


class UserMovieWishlist(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='wishlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-created_at']

