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
│   │   ├── models.py        # User 모델 (AbstractUser 상속)
│   │   ├── views.py         # 인증 뷰 (회원가입, 로그인, 프로필)
│   │   ├── serializers.py   # 사용자 시리얼라이저
│   │   └── urls.py          # 인증 URL 라우팅
│   ├── movies/              # 영화 데이터 앱 (현재 미사용)
│   ├── config/              # Django 설정
│   │   ├── settings.py      # 프로젝트 설정 (JWT, CORS 등)
│   │   └── urls.py          # 메인 URL 설정
│   └── manage.py
├── frontend/                # Vue 프로젝트
│   ├── src/
│   │   ├── components/      # Vue 컴포넌트
│   │   │   └── NavBar.vue   # 네비게이션 바 (햄버거 메뉴 포함)
│   │   ├── views/          # 페이지 뷰
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── MovieDetailView.vue
│   │   │   ├── MovieReviewsView.vue
│   │   │   ├── ProfileView.vue
│   │   │   ├── ProfileEditView.vue
│   │   │   ├── ProfileEmotionsView.vue
│   │   │   └── ProfileReviewsView.vue
│   │   ├── router/         # 라우터 설정
│   │   ├── stores/         # Pinia 스토어 (auth)
│   │   ├── api/            # API 클라이언트 (Axios 인터셉터)
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
- 로그인 (이메일 기반 인증)
- JWT 토큰 기반 인증 (Access Token: 1분, Refresh Token: 30일)
- 자동 토큰 갱신 (API 인터셉터)
- 토큰 만료 시 자동 로그아웃 및 알림
- 프로필 조회/수정
  - 닉네임 수정
  - 프로필 이미지 업로드/수정
  - 비밀번호 변경
  - 이메일 수정 불가 (보안 정책)
- 로그아웃 기능
- 로그인 에러 메시지 개선 (이메일/비밀번호 구분)

### 2. 프로필 관리
- 프로필 페이지 (`/profile`)
  - 사용자 정보 표시 (닉네임, 이메일, 프로필 이미지, 가입일)
  - 메뉴 버튼: 회원정보 수정, 감정 분석 기록, 리뷰
- 회원정보 수정 페이지 (`/profile/edit`)
  - 닉네임, 프로필 이미지, 비밀번호 수정 가능
  - 이미지 미리보기 기능
  - FormData를 통한 파일 업로드
- 감정 분석 기록 페이지 (`/profile/emotions`) - 준비 중
- 리뷰 페이지 (`/profile/reviews`) - 준비 중

### 3. 영화 데이터
- 인기 영화 목록 조회
- 영화 상세 정보 조회
- TMDB API 연동 준비
- ⚠️ **참고**: `movies` 앱은 현재 미사용 중 (다른 팀원이 담당)

### 4. 리뷰
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
  - 응답: `{ user, tokens: { access, refresh } }`
- `POST /api/v1/accounts/login/` - 로그인 (이메일 기반)
  - 요청: `{ email, password }`
  - 응답: `{ user, tokens: { access, refresh } }`
  - 에러: 이메일/비밀번호 구분된 에러 메시지
- `GET /api/v1/accounts/profile/` - 프로필 조회 (인증 필요)
  - 응답: `{ id, username, email, nickname, profile_image, created_at }`
- `PATCH /api/v1/accounts/profile/update/` - 프로필 수정 (인증 필요)
  - 요청: `FormData { nickname, profile_image, new_password, password_confirm }`
  - 이메일 수정 불가 (보안 정책)
- `POST /api/v1/accounts/token/refresh/` - 토큰 갱신
  - 요청: `{ refresh: "refresh_token" }`
  - 응답: `{ access: "new_access_token" }`

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
- 이메일과 비밀번호로 로그인 (이메일 기반 인증)
- JWT 토큰 기반 인증
- 로그인 성공 시 홈으로 리다이렉트
- 로그인 실패 시 에러 메시지 표시 (이메일/비밀번호 구분)
- 토큰 만료 시 자동 로그아웃 알림 팝업

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

### 6. 프로필 페이지 (/profile)
- 사용자 정보 표시 (프로필 이미지, 닉네임, 이메일, 가입일)
- 메뉴 버튼:
  - 회원정보 수정 → `/profile/edit`
  - 감정 분석 기록 → `/profile/emotions` (준비 중)
  - 리뷰 → `/profile/reviews` (준비 중)
- 뒤로가기 버튼 (메인 페이지로 이동)

### 7. 회원정보 수정 페이지 (/profile/edit)
- 닉네임 수정
- 프로필 이미지 업로드/수정 (미리보기 기능)
- 비밀번호 변경 (선택사항)
- 이메일 수정 불가 (보안 정책)
- 수정 완료 시 프로필 페이지로 자동 이동

### 8. 감정 분석 기록 페이지 (/profile/emotions)
- 준비 중 (다른 팀원이 구현 예정)

### 9. 리뷰 페이지 (/profile/reviews)
- 준비 중

## 최근 업데이트 내역

### 2024년 업데이트
- ✅ **로그인 시스템 개선**: username 기반에서 email 기반 인증으로 변경
- ✅ **회원 정보 API**: 프로필 조회/수정 API 완료
- ✅ **로그아웃 기능**: NavBar에 로그아웃 버튼 추가 및 기능 구현
- ✅ **API 인터셉터 개선**: 로그인/회원가입 API는 인터셉터에서 제외하여 리다이렉트 문제 해결
- ✅ **가상환경 설정**: venv 가상환경 사용 권장 (`.gitignore`에 포함)
- ✅ **프로필 기능 구현**: 프로필 페이지, 회원정보 수정 페이지 추가
  - 프로필 이미지 업로드/수정 기능
  - 닉네임, 비밀번호 수정 기능
  - 이메일 수정 불가 정책 적용
- ✅ **JWT 토큰 설정**: Access Token 1분, Refresh Token 30일로 설정
- ✅ **토큰 만료 처리**: 토큰 갱신 실패 시 자동 로그아웃 및 알림 팝업
- ✅ **로그인 에러 개선**: 이메일/비밀번호 구분된 에러 메시지
- ✅ **NavBar 개선**: 
  - 햄버거 메뉴 추가 (반응형 디자인)
  - 프로필 링크 추가 (로그인 시 사용자 닉네임 표시)
  - 스타일 개선 (검정 테두리, hover 효과)
- ✅ **데이터베이스 정리**: 
  - `users` 테이블 삭제, `accounts_user` 테이블 사용
  - 불필요한 마이그레이션 스크립트 삭제
  - `init_sqlite_database.sql` 파일 삭제 (Django migrations로 테이블 관리)
- ✅ **계정 비활성화 제거**: `is_active` 체크 제거, 직접 삭제 방식 채택
- ✅ **모킹 데이터 제거**: 
  - `auth.js`에서 모킹 데이터 코드 제거
  - 백엔드 API 통신만 사용하도록 정리

## 주의사항

1. **API 키 보안**: TMDB API 키는 `.env` 파일에 저장하고 절대 공개 저장소에 커밋하지 마세요.
2. **CORS 설정**: 프론트엔드와 백엔드가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.
3. **환경 변수**: `.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.
4. **가상환경**: 백엔드 개발 시 venv 가상환경 사용을 권장합니다.

## 참고 사이트

- [TMDB API](https://www.themoviedb.org/documentation/api)
- [왓챠피디아](https://pedia.watcha.com/ko-KR/)

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
