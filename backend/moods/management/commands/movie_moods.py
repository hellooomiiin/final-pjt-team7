# moods/management/commands/analyze_emotions.py
from django.core.management.base import BaseCommand
from movies.models import Movie
from moods.models import MovieMood
from transformers import pipeline # pip install transformers torch 필요
from tqdm import tqdm # 진행률 표시바 (pip install tqdm)

class Command(BaseCommand):
		help = '영화 영문 줄거리를 AI로 분석하여 감정 데이터를 저장합니다.'

		def handle(self, *args, **options):
				# 1. 분석할 영화 가져오기 (이미 분석된 건 제외하고, 영문 줄거리가 있는 것만)
				movies = Movie.objects.filter(mood_result__isnull=True).exclude(overview_en='')
				
				if not movies.exists():
						self.stdout.write(self.style.SUCCESS('분석할 새로운 영화가 없습니다.'))
						return

				self.stdout.write(f'총 {movies.count()}개의 영화 분석을 시작합니다...')

				# 2. AI 모델 로드 (Hugging Face)
				# 추천드렸던 28가지 감정 모델 사용
				classifier = pipeline(
						task="text-classification", 
						model="SamLowe/roberta-base-go_emotions", 
						top_k=None, # 모든 감정 점수 다 가져오기
						truncation=True # 긴 줄거리 잘라서 에러 방지
				)

				# 3. 하나씩 분석 후 저장
				for movie in tqdm(movies):
					try:
						# 줄거리 분석 실행
						outputs = classifier(movie.overview_en)
						# outputs 예시: [[{'label': 'realization', 'score': 0.8}, ...]]
						
						scores = outputs[0] # 첫 번째 결과 리스트
						# scores 예시: [
						#   {'label': 'neutral', 'score': 0.85}, 
						#   {'label': 'sadness', 'score': 0.12}, 
						#   {'label': 'fear', 'score': 0.03}
						# ]

						# [수정된 로직] neutral 건너뛰기
						dominant_mood = None
						
						for mood in scores:
								if mood['label'] == 'neutral':
										continue # 뉴트럴이면 다음 껄로 넘어감
								
								# 뉴트럴이 아닌 것 중 점수가 가장 높은 것 당첨
								dominant_mood = mood['label']
								break
						
						# 만약 모든게 neutral이거나 점수가 너무 낮으면? (안전장치)
						if not dominant_mood:
								dominant_mood = 'neutral' # 어쩔 수 없이 neutral 저장

						# DB 저장
						MovieMood.objects.create(
								movie=movie,
								dominant_mood=dominant_mood, # 2등이 저장됨 (예: sadness)
								score_details=scores
						)

					except Exception as e:
						self.stdout.write(self.style.ERROR(f'Error analyzing {movie.title}: {str(e)}'))

				self.stdout.write(self.style.SUCCESS('모든 영화의 감정 분석이 완료되었습니다!'))