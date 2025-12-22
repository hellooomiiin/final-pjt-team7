# 영화 추천 커뮤니티 서비스 (개발 중)

영화 추천 커뮤니티 서비스의 기본 뼈대입니다. 현재는 메인 페이지, 사용자 인증, 영화 상세 페이지, 영화별 리뷰 페이지가 구현되어 있으며, 향후 기능별로 확장 예정입니다.

## 기술 스택

### Backend
- Django 5.2
- Django REST Framework
- Python 3.11
- SQLite

### Frontend
- Vue 3
- Vue Router
- Axios
- Bootstrap 5.3
- Vite

## 프로젝트 구조

```
final-pjt-team7/
├── backend/                 # Django 프로젝트
│   ├── accounts/            # 사용자 인증 앱
│   ├── movies/              # 영화 데이터 앱
│   ├── config/              # Django 설정
│   └── manage.py
├── frontend/                # Vue 프로젝트
│   ├── src/
│   │   ├── components/      # Vue 컴포넌트 (NavBar)
│   │   ├── views/          # 페이지 뷰 (Home, Login, Register, MovieDetail, MovieReviews)
│   │   ├── router/         # 라우터 설정
│   │   ├── stores/         # Pinia 스토어 (auth)
│   │   ├── api/            # API 클라이언트
│   │   └── data/           # Mock 데이터
│   └── package.json
└── README.md
```

## 설치 및 실행

### Backend 설정

1. 가상환경 생성 및 활성화
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
```bash
# backend/.env 파일 생성
SECRET_KEY=your-secret-key-here
DEBUG=True
TMDB_API_KEY=your-tmdb-api-key-here
```

4. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

6. 서버 실행
```bash
python manage.py runserver
```

### Frontend 설정

1. 의존성 설치
```bash
cd frontend
npm install
```

2. 환경 변수 설정
```bash
# frontend/.env 파일 생성
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

3. 개발 서버 실행
```bash
npm run dev
```

## 주요 기능

### 1. 사용자 인증
- 회원가입 (이름, 닉네임, 이메일, 비밀번호)
- 로그인 (이메일 기반)
- JWT 토큰 기반 인증
- 프로필 조회/수정

### 2. 영화 데이터
- 인기 영화 목록 조회
- 영화 상세 정보 조회
- TMDB API 연동 준비

### 3. 리뷰
- 영화 상세 페이지에서 리뷰 미리보기 (상위 3개, 최신순 정렬)
- 영화별 리뷰 페이지에서 해당 영화의 모든 리뷰 조회
- 리뷰 정렬 필터 (기본값: 최신순)
  - 좋아요 순
  - 높은 평가 순
  - 낮은 평가 순
  - 최신 순
  - 오래된 순
- 리뷰 좋아요 기능
- 페이지네이션

## 데이터베이스 테이블 구조

### accounts 앱
- **accounts_user**: 사용자 정보
  - username, email, nickname, profile_image
  - password, created_at, updated_at
  - AbstractUser 상속 필드들 (is_staff, is_active 등)

### movies 앱
- **movies_genre**: 장르 정보
- **movies_movie**: 영화 정보
- **movies_person**: 인물 정보 (배우, 제작진)
- **movies_moviecast**: 영화-배우 관계
- **movies_moviecrew**: 영화-제작진 관계
- **movies_moviekeyword**: 영화 키워드
- **movies_movieimage**: 영화 이미지
- **movies_movievideo**: 영화 비디오 (예고편 등)
- **movies_usermoviewishlist**: 사용자 위시리스트

## API 엔드포인트

### 인증 (accounts)
- `POST /api/v1/accounts/register/` - 회원가입
  - 요청: `{ username, email, nickname, password, password_confirm }`
- `POST /api/v1/accounts/login/` - 로그인
  - 요청: `{ username, password }`
- `GET /api/v1/accounts/profile/` - 프로필 조회 (인증 필요)
- `PUT /api/v1/accounts/profile/update/` - 프로필 수정 (인증 필요)
- `POST /api/v1/accounts/token/refresh/` - 토큰 갱신

### 영화 (movies)
- `GET /api/v1/movies/popular/` - 인기 영화 목록 (상위 20개)
- `GET /api/v1/movies/` - 영화 목록 조회
- `GET /api/v1/movies/{id}/` - 영화 상세 정보 조회

## 화면 구성

### 1. 메인 페이지 (/)
- 인기 영화 카드 표시
- 네비게이션 바 (홈, 로그인, 회원가입 버튼)
- 인기 영화 카드 클릭 시 영화 상세 페이지로 이동

### 2. 로그인 페이지 (/login)
- 이메일과 비밀번호로 로그인
- JWT 토큰 기반 인증
- 로그인 성공 시 홈으로 리다이렉트

### 3. 회원가입 페이지 (/register)
- 이름, 닉네임, 이메일, 비밀번호 입력
- 회원가입 성공 시 로그인 페이지로 리다이렉트

### 4. 영화 상세 페이지 (/movies/:id)
- 영화 포스터, 제목, 원제, 줄거리, 평점 등 상세 정보 표시
- 리뷰 섹션 (상위 3개 미리보기, 최신순 정렬)
- "더보기 →" 버튼 클릭 시 해당 영화의 리뷰 페이지로 이동

### 5. 영화별 리뷰 페이지 (/movies/:id/reviews)
- 해당 영화의 모든 리뷰 조회
- 영화 정보 헤더 (포스터, 제목)
- 리뷰 정렬 필터 (드롭다운):
  - 최신 순 (기본값)
  - 오래된 순
  - 좋아요 순
  - 높은 평가 순
  - 낮은 평가 순
- 리뷰 좋아요 기능 (하트 버튼)
- 리뷰 카드에 작성자, 작성일, 평점, 좋아요 수 표시
- 뒤로가기 버튼

## 주의사항

1. **API 키 보안**: TMDB API 키는 `.env` 파일에 저장하고 절대 공개 저장소에 커밋하지 마세요.
2. **CORS 설정**: 프론트엔드와 백엔드가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.
3. **환경 변수**: `.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.

## 참고 사이트

- [TMDB API](https://www.themoviedb.org/documentation/api)
- [왓챠피디아](https://pedia.watcha.com/ko-KR/)

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
