# 라이브러리 설치 필요: pip install transformers torch

from transformers import pipeline

# 1. 파이프라인 생성 (자동으로 모델 다운로드)
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# 2. 영화 줄거리 예시 (타이타닉)
movie_overview = "Are you crazy? this is insane! I have to get out of here."

# 3. 감정 분석 실행
model_outputs = classifier(movie_overview)

# 4. 결과 출력 (상위 3개 감정)
# 결과값 예시: [{'label': 'neutral', 'score': 0.x}, {'label': 'sadness', 'score': 0.x}, ...]
print(model_outputs)
