# Backend (Django REST Framework)

## 설치 및 실행

1. 가상환경 생성
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
TMDB_API_KEY=your-tmdb-api-key-here
```

4. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 감정 데이터 초기화
```bash
python manage.py init_emotions
```

6. 서버 실행
```bash
python manage.py runserver
```

## API 문서

서버 실행 후 다음 URL에서 API를 테스트할 수 있습니다:
- http://localhost:8000/api/v1/

