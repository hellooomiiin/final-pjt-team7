import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from .models import (
    Movie, Genre, Person, MovieCast, MovieCrew,
    MovieKeyword, MovieImage, MovieVideo
)


class TMDBService:
    BASE_URL = 'https://api.themoviedb.org/3'
    IMAGE_BASE_URL = 'https://image.tmdb.org/t/p'

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        if not self.api_key:
            raise ValueError("TMDB_API_KEY가 설정되지 않았습니다.")

    def _get(self, endpoint, params=None):
        """TMDB API GET 요청"""
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params['api_key'] = self.api_key
        params['language'] = 'ko-KR'
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_poster_url(self, path):
        """포스터 이미지 URL 생성"""
        if not path:
            return None
        return f"{self.IMAGE_BASE_URL}/w500{path}"

    def _get_backdrop_url(self, path):
        """배경 이미지 URL 생성"""
        if not path:
            return None
        return f"{self.IMAGE_BASE_URL}/original{path}"

    def _parse_date(self, date_str):
        """날짜 문자열을 Date 객체로 변환"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return None

    def get_or_create_genres(self):
        """장르 데이터 가져오기 및 생성"""
        data = self._get('/genre/movie/list')
        genres = []
        for genre_data in data.get('genres', []):
            genre, _ = Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
            genres.append(genre)
        return genres

    def get_or_create_person(self, person_data):
        """인물 데이터 가져오기 및 생성"""
        person, _ = Person.objects.get_or_create(
            tmdb_id=person_data['id'],
            defaults={
                'name': person_data.get('name', ''),
                'profile_path': self._get_poster_url(person_data.get('profile_path')),
                'biography': person_data.get('biography', ''),
                'birthday': self._parse_date(person_data.get('birthday')),
                'place_of_birth': person_data.get('place_of_birth', ''),
            }
        )
        return person

    def get_or_create_movie(self, tmdb_id):
        """영화 데이터 가져오기 및 생성"""
        # 기본 정보
        movie_data = self._get(f'/movie/{tmdb_id}')
        
        # 추가 정보
        credits_data = self._get(f'/movie/{tmdb_id}/credits')
        keywords_data = self._get(f'/movie/{tmdb_id}/keywords')
        images_data = self._get(f'/movie/{tmdb_id}/images')
        videos_data = self._get(f'/movie/{tmdb_id}/videos')

        # 영화 생성 또는 업데이트
        movie, created = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': movie_data.get('title', ''),
                'original_title': movie_data.get('original_title', ''),
                'overview': movie_data.get('overview', ''),
                'release_date': self._parse_date(movie_data.get('release_date')),
                'poster_path': self._get_poster_url(movie_data.get('poster_path')),
                'backdrop_path': self._get_backdrop_url(movie_data.get('backdrop_path')),
                'vote_average': movie_data.get('vote_average'),
                'vote_count': movie_data.get('vote_count', 0),
                'popularity': movie_data.get('popularity', 0.0),
                'runtime': movie_data.get('runtime'),
                'tagline': movie_data.get('tagline', ''),
            }
        )

        if not created:
            # 기존 영화 업데이트
            movie.title = movie_data.get('title', movie.title)
            movie.original_title = movie_data.get('original_title', movie.original_title)
            movie.overview = movie_data.get('overview', movie.overview)
            movie.release_date = self._parse_date(movie_data.get('release_date')) or movie.release_date
            movie.poster_path = self._get_poster_url(movie_data.get('poster_path')) or movie.poster_path
            movie.backdrop_path = self._get_backdrop_url(movie_data.get('backdrop_path')) or movie.backdrop_path
            movie.vote_average = movie_data.get('vote_average', movie.vote_average)
            movie.vote_count = movie_data.get('vote_count', movie.vote_count)
            movie.popularity = movie_data.get('popularity', movie.popularity)
            movie.runtime = movie_data.get('runtime', movie.runtime)
            movie.tagline = movie_data.get('tagline', movie.tagline)
            movie.save()

        # 장르 연결
        genre_ids = [g['id'] for g in movie_data.get('genres', [])]
        genres = Genre.objects.filter(tmdb_id__in=genre_ids)
        movie.genres.set(genres)

        # 출연진 및 제작진
        # Cast
        MovieCast.objects.filter(movie=movie).delete()
        for idx, cast_data in enumerate(credits_data.get('cast', [])[:20]):  # 상위 20명만
            person = self.get_or_create_person(cast_data)
            MovieCast.objects.create(
                movie=movie,
                person=person,
                character=cast_data.get('character', ''),
                order=idx
            )

        # Crew
        MovieCrew.objects.filter(movie=movie).delete()
        for crew_data in credits_data.get('crew', []):
            person = self.get_or_create_person(crew_data)
            MovieCrew.objects.create(
                movie=movie,
                person=person,
                job=crew_data.get('job', ''),
                department=crew_data.get('department', '')
            )

        # 키워드
        keyword_ids = [k['id'] for k in keywords_data.get('keywords', [])]
        keywords = []
        for keyword_data in keywords_data.get('keywords', []):
            keyword, _ = MovieKeyword.objects.get_or_create(
                tmdb_id=keyword_data['id'],
                defaults={'name': keyword_data['name']}
            )
            keywords.append(keyword)
        movie.keywords.set(keywords)

        # 이미지
        MovieImage.objects.filter(movie=movie).delete()
        for image_data in images_data.get('backdrops', [])[:10]:  # 상위 10개만
            MovieImage.objects.create(
                movie=movie,
                file_path=self._get_backdrop_url(image_data.get('file_path')),
                aspect_ratio=image_data.get('aspect_ratio'),
                height=image_data.get('height'),
                width=image_data.get('width'),
                vote_average=image_data.get('vote_average'),
                vote_count=image_data.get('vote_count', 0)
            )

        # 영상
        MovieVideo.objects.filter(movie=movie).delete()
        for video_data in videos_data.get('results', []):
            if video_data.get('site') == 'YouTube':
                MovieVideo.objects.create(
                    movie=movie,
                    key=video_data.get('key', ''),
                    name=video_data.get('name', ''),
                    site=video_data.get('site', 'YouTube'),
                    type=video_data.get('type', ''),
                    official=video_data.get('official', False)
                )

        return movie

    def update_movie_details(self, tmdb_id):
        """영화 상세 정보 업데이트"""
        return self.get_or_create_movie(tmdb_id)

    def search_movies(self, query):
        """영화 검색"""
        data = self._get('/search/movie', params={'query': query})
        results = []
        for movie_data in data.get('results', [])[:10]:  # 상위 10개만
            movie = self.get_or_create_movie(movie_data['id'])
            results.append({
                'id': movie.id,
                'tmdb_id': movie.tmdb_id,
                'title': movie.title,
                'poster_path': movie.poster_path,
                'release_date': movie.release_date,
                'vote_average': movie.vote_average,
            })
        return results

    def get_popular_movies(self, page=1):
        """인기 영화 목록 가져오기"""
        data = self._get('/movie/popular', params={'page': page})
        movies = []
        for movie_data in data.get('results', []):
            movie = self.get_or_create_movie(movie_data['id'])
            movies.append(movie)
        return movies

