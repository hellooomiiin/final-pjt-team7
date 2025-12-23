import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre

class Command(BaseCommand):
    help = 'TMDb 영화 데이터 수집 (상세 정보 포함)'

    def handle(self, *args, **options):
        api_key = settings.TMDB_API_KEY
        
        # 1. 장르 데이터 수집 (기존과 동일)
        self.stdout.write('장르 데이터 수집 중...')
        genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko-KR"
        genres = requests.get(genre_url).json().get('genres', [])
        for genre_data in genres:
            Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )

        # 2. 영화 데이터 수집
        self.stdout.write('영화 데이터 수집 중...')
        
        # 인기 영화 5페이지만 수집 (너무 많이 하면 시간이 오래 걸립니다)
        for page in range(1, 6):
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}"
            response = requests.get(url)
            results = response.json().get('results', [])

            for movie_data in results:
                movie_id = movie_data['id']
                
                # [핵심] 영화 상세 정보 + 출연진(credits) 추가 호출
                detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR&append_to_response=credits"
                detail_res = requests.get(detail_url).json()

                # 2-1. 감독 찾기 (Crew 리스트에서 job이 Director인 사람)
                director_name = "Unknown"
                if 'credits' in detail_res and 'crew' in detail_res['credits']:
                    crew_list = detail_res['credits']['crew']
                    # 파이썬의 next 함수로 첫 번째 감독만 빠르게 찾기
                    director_entry = next((person for person in crew_list if person['job'] == 'Director'), None)
                    if director_entry:
                        director_name = director_entry['name']

                # 2-2. 배우 찾기 (Cast 리스트에서 상위 5명만 추출)
                actors_list = []
                if 'credits' in detail_res and 'cast' in detail_res['credits']:
                    # 최대 5명까지만 저장
                    for cast in detail_res['credits']['cast'][:5]:
                        actors_list.append({
                            'name': cast['name'],
                            'character': cast['character'],
                            'profile_path': cast['profile_path'] # 배우 사진
                        })

                # 2-3. 개봉일 빈 값 처리
                release_date = movie_data.get('release_date') or None

                # 2-4. DB 저장
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_id,
                    defaults={
                        'title': movie_data['title'],
                        'overview': movie_data['overview'],
                        'poster_path': movie_data['poster_path'],
                        'release_date': release_date,
                        'popularity': movie_data['popularity'],
                        'vote_average': movie_data['vote_average'],
                        'vote_count': movie_data['vote_count'],
                        # [추가된 부분]
                        'runtime': detail_res.get('runtime'),
                        'director': director_name,
                        'actors': actors_list
                    }
                )

                # 2-5. 장르 연결
                movie.genres.clear()
                for genre_id in movie_data.get('genre_ids', []):
                    try:
                        genre = Genre.objects.get(tmdb_id=genre_id)
                        movie.genres.add(genre)
                    except Genre.DoesNotExist:
                        pass
                
                self.stdout.write(f"Updated: {movie.title}")

        self.stdout.write(self.style.SUCCESS('데이터 수집 완료!'))