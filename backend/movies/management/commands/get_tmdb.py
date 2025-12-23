import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre

class Command(BaseCommand):
    help = 'TMDb API에서 영화 데이터와 장르 데이터를 가져와 DB에 저장합니다.'

    def handle(self, *args, **options):
        api_key = settings.TMDB_API_KEY
        
        if not api_key:
            self.stdout.write(self.style.ERROR('settings.py에 TMDB_API_KEY가 설정되지 않았습니다.'))
            return

        # 1. 장르 데이터 가져오기 (Genres First)
        # 영화 저장 시 장르 연결을 위해 장르 데이터가 먼저 DB에 있어야 합니다.
        self.stdout.write('장르 데이터 수집 시작...')
        genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko-KR"
        response = requests.get(genre_url)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'장르 데이터를 가져오는데 실패했습니다.'))
            self.stdout.write(self.style.ERROR(f'상태 코드: {response.status_code}'))
            self.stdout.write(self.style.ERROR(f'에러 메시지: {response.text}'))
            return

        genres = response.json().get('genres', [])
        for genre_data in genres:
            # get_or_create: 이미 있으면 가져오고, 없으면 생성 (중복 방지)
            Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
        
        self.stdout.write(self.style.SUCCESS(f'{len(genres)}개의 장르 데이터 저장 완료.'))


        # 2. 영화 데이터 가져오기 (Movies)
        # 인기 영화 목록을 페이지 단위로 가져옵니다. (여기서는 예시로 1~5페이지, 약 100개)
        self.stdout.write('영화 데이터 수집 시작...')
        total_movies = 0
        
        for page in range(1, 6): # 1페이지부터 5페이지까지 반복
            movie_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}"
            response = requests.get(movie_url)
            
            if response.status_code != 200:
                self.stdout.write(self.style.WARNING(f'{page}페이지를 가져오는데 실패했습니다.'))
                continue

            movies = response.json().get('results', [])
            
            for movie_data in movies:
                # 2-1. 개봉일 데이터 전처리 (빈 문자열이면 None 처리)
                release_date = movie_data.get('release_date')
                if not release_date:
                    release_date = None

                # 2-2. 영화 저장 (update_or_create 사용)
                # 이미 있는 영화라면 정보를 갱신하고, 없으면 새로 만듭니다.
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data['title'],
                        'overview': movie_data['overview'],
                        'poster_path': movie_data['poster_path'],
                        'release_date': release_date,
                        'popularity': movie_data['popularity'],
                        'vote_average': movie_data['vote_average'],
                        'vote_count': movie_data['vote_count'],
                    }
                )

                # 2-3. 영화-장르 관계 설정 (Many-to-Many)
                # TMDb는 genre_ids라는 리스트(예: [28, 12])를 줍니다.
                movie.genres.clear() # 기존 장르 연결 초기화 (업데이트 시 중복 방지)
                for genre_id in movie_data.get('genre_ids', []):
                    try:
                        genre = Genre.objects.get(tmdb_id=genre_id)
                        movie.genres.add(genre) # 관계 테이블(movie_genres)에 데이터 자동 추가
                    except Genre.DoesNotExist:
                        # 간혹 TMDb 영화 데이터에는 있는데 장르 목록에는 없는 ID가 있을 수 있음
                        pass
                
                total_movies += 1

        self.stdout.write(self.style.SUCCESS(f'총 {total_movies}개의 영화 데이터를 성공적으로 저장했습니다!'))