# Backend (Django REST Framework)

## 기술 스택

- Django 5.2
- Django REST Framework
- Django CORS Headers
- Python Decouple (환경 변수 관리)
- SQLite (개발용 데이터베이스)

## 프로젝트 구조

```
backend/
├── accounts/                 # 사용자 인증 앱
│   ├── models.py            # User 모델 (AbstractUser 상속)
│   ├── serializers.py       # 사용자 시리얼라이저
│   ├── views.py             # 인증 뷰셋
│   └── urls.py              # 인증 URL 라우팅
├── movies/                   # 영화 데이터 앱
│   ├── models.py            # Movie, Genre, Person 등 모델
│   ├── serializers.py       # 영화 시리얼라이저
│   ├── views.py             # 영화 뷰셋
│   └── urls.py              # 영화 URL 라우팅
├── config/                   # Django 설정
│   ├── settings.py          # 프로젝트 설정
│   ├── urls.py              # 메인 URL 설정
│   ├── wsgi.py              # WSGI 설정
│   └── asgi.py              # ASGI 설정
└── manage.py
```

## 설치 및 실행

1. 가상환경 생성
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 또는
source venv/bin/activate  # Linux/Mac
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

5. 감정 데이터 초기화 (선택사항)
```bash
python manage.py init_emotions
```

6. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

7. 서버 실행
```bash
python manage.py runserver
```

서버는 http://localhost:8000 에서 실행됩니다.

## API 엔드포인트

### 인증 (accounts)
- `POST /api/v1/accounts/register/` - 회원가입
  - 요청: `{ username, email, nickname, password, password_confirm }`
  - 응답: `{ user, tokens: { access, refresh } }`
- `POST /api/v1/accounts/login/` - 로그인 (이메일 기반)
  - 요청: `{ email, password }`
  - 응답: `{ user, tokens: { access, refresh } }`
- `GET /api/v1/accounts/profile/` - 프로필 조회 (인증 필요)
  - 응답: `{ id, username, email, nickname, profile_image, created_at }`
- `PUT /api/v1/accounts/profile/` - 프로필 수정 (인증 필요)
- `PATCH /api/v1/accounts/profile/` - 프로필 부분 수정 (인증 필요)
- `PUT /api/v1/accounts/profile/update/` - 프로필 수정 (인증 필요)
- `POST /api/v1/accounts/token/refresh/` - JWT 토큰 갱신

### 영화 (movies)
- `GET /api/v1/movies/` - 영화 목록 조회
- `GET /api/v1/movies/popular/` - 인기 영화 목록 (상위 20개)
- `GET /api/v1/movies/{id}/` - 영화 상세 정보 조회

### 리뷰 (reviews)
- `GET /api/v1/reviews/` - 리뷰 목록 조회
  - 쿼리 파라미터: `movie={movie_id}`, `ordering={정렬옵션}`
- `POST /api/v1/reviews/` - 리뷰 작성 (인증 필요)
- `GET /api/v1/reviews/{id}/` - 리뷰 상세 조회
- `PUT /api/v1/reviews/{id}/` - 리뷰 수정 (인증 필요)
- `DELETE /api/v1/reviews/{id}/` - 리뷰 삭제 (인증 필요)
- `POST /api/v1/reviews/{id}/like/` - 리뷰 좋아요 (인증 필요)
- `DELETE /api/v1/reviews/{id}/like/` - 리뷰 좋아요 취소 (인증 필요)

## API 문서

서버 실행 후 다음 URL에서 API를 테스트할 수 있습니다:
- http://localhost:8000/api/v1/
- Django Admin: http://localhost:8000/admin/ (슈퍼유저 필요)

## 최근 업데이트 내역

### 2024년 업데이트
- ✅ **로그인 시스템**: email 기반 인증으로 변경 (기존 username 기반에서 변경)
- ✅ **회원 정보 API**: 프로필 조회/수정 API 완료
  - `GET /api/v1/accounts/profile/` - 프로필 조회
  - `PUT/PATCH /api/v1/accounts/profile/` - 프로필 수정
- ✅ **인증 로직**: `authenticate()` 대신 email로 직접 사용자 조회 후 `check_password()` 사용

## 주의사항

1. **개발 서버 경고**: `runserver`는 개발용입니다. 프로덕션 환경에서는 Gunicorn, uWSGI 등의 WSGI 서버를 사용하세요.
2. **CORS 설정**: 프론트엔드와 백엔드가 다른 포트에서 실행되므로 `django-cors-headers`가 설정되어 있습니다.
3. **환경 변수**: `.env` 파일은 절대 공개 저장소에 커밋하지 마세요.
4. **가상환경**: venv 가상환경 사용을 권장합니다. `.gitignore`에 포함되어 있어 커밋되지 않습니다.

