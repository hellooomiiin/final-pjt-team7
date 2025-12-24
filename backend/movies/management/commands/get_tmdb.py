import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre

class Command(BaseCommand):
    help = 'TMDb 영화 데이터 수집 (상세 정보 포함)'

    def handle(self, *args, **options):
        api_key = settings.TMDB_API_KEY
        
        # [설정] 필터링 기준값
        MIN_VOTE_COUNT = 100   # 최소 투표 수 (이것보다 적으면 거름)
        MIN_VOTE_AVERAGE = 4.0 # 최소 평점
        
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
        
        for page in range(1, 10):
            # 2-1. 목록 가져오기 (한국어 기준)
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}"
            response = requests.get(url)
            results = response.json().get('results', [])

            for movie_data in results:
                if movie_data['vote_count'] < MIN_VOTE_COUNT:
                    self.stdout.write(self.style.WARNING(f"Skipped (Low Votes): {movie_data['title']} ({movie_data['vote_count']})"))
                    continue
                
                if not movie_data['overview']:
                    self.stdout.write(self.style.WARNING(f"Skipped (No Overview): {movie_data['title']}"))
                    continue
                
                movie_id = movie_data['id']
                
                # ---------------------------------------------------------
                # 한국어 상세 정보 가져오기 (감독, 배우용)
                detail_url_ko = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR&append_to_response=credits"
                detail_res_ko = requests.get(detail_url_ko).json()

                # 영어 상세 정보 가져오기 (오직 줄거리용 ⭐)
                # language='en-US'로 설정해서 확실한 영어 원문
                detail_url_en = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=keywords"
                detail_res_en = requests.get(detail_url_en).json()
                
                overview_raw = detail_res_en.get('overview', '')
                tagline_raw = detail_res_en.get('tagline', '')
                
                # 2. 키워드 추출 (리스트 형태 -> 문자열로 변환)
                # 예: ['prison', 'escape'] -> "prison, escape"
                keywords_data = detail_res_en.get('keywords', {}).get('keywords', [])
                keywords_list = [k['name'] for k in keywords_data]
                keywords_str = ", ".join(keywords_list)
                
                # 3. 텍스트 합치기 (태그라인 -> 줄거리 -> 키워드 순서)
                full_text_parts = []
                
                if tagline_raw:
                    full_text_parts.append(f"{tagline_raw}.")  # 태그라인 끝에 마침표 추가
                
                if overview_raw:
                    full_text_parts.append(overview_raw)
                
                if keywords_str:
                    full_text_parts.append(f"Keywords: {keywords_str}.") # 키워드임을 명시
                
                # 공백으로 이어 붙이기
                overview_en = " ".join(full_text_parts)
                
                # 4. 만약 다 합쳤는데도 빈 값이면 한국어 줄거리로 대체 (방어 코드)
                if not overview_en.strip():
                    overview_en = movie_data['overview']
                # ---------------------------------------------------------

                # 2-3. 감독 & 배우 찾기 (한국어 응답 기준)
                director_name = "Unknown"
                if 'credits' in detail_res_ko and 'crew' in detail_res_ko['credits']:
                    crew_list = detail_res_ko['credits']['crew']
                    director_entry = next((person for person in crew_list if person['job'] == 'Director'), None)
                    if director_entry:
                        director_name = director_entry['name']

                actors_list = []
                if 'credits' in detail_res_ko and 'cast' in detail_res_ko['credits']:
                    for cast in detail_res_ko['credits']['cast'][:5]:
                        actors_list.append({
                            'name': cast['name'],
                            'character': cast['character'],
                            'profile_path': cast['profile_path']
                        })

                # 2-4. 개봉일 빈 값 처리
                release_date = movie_data.get('release_date') or None

                # 2-5. DB 저장
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_id,
                    defaults={
                        'title': movie_data['title'],
                        'overview': movie_data['overview'],
                        'overview_en': overview_en, # [확인] 이제 확실한 영어가 들어갑니다!
                        'poster_path': movie_data['poster_path'],
                        'release_date': release_date,
                        'popularity': movie_data['popularity'],
                        'vote_average': movie_data['vote_average'],
                        'vote_count': movie_data['vote_count'],
                        'runtime': detail_res_ko.get('runtime'), # 런타임은 한국어 응답에서
                        'director': director_name,
                        'actors': actors_list
                    }
                )

                # 2-6. 장르 연결 (기존 동일)
                movie.genres.clear()
                for genre_id in movie_data.get('genre_ids', []):
                    try:
                        genre = Genre.objects.get(tmdb_id=genre_id)
                        movie.genres.add(genre)
                    except Genre.DoesNotExist:
                        pass
                
                self.stdout.write(f"Updated: {movie.title} (EN Overview Length: {len(overview_en)}) (Keywords: {len(keywords_list)})")

        self.stdout.write(self.style.SUCCESS('데이터 수집 완료!'))