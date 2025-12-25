# 영화 추천 커뮤니티 서비스 (Mood-Match)

감정 기반 영화 추천 커뮤니티 서비스입니다. 사용자의 현재 기분에 맞는 영화를 AI로 분석하여 추천하고, 영화에 대한 리뷰와 댓글을 작성할 수 있는 플랫폼입니다.

## 주요 특징
- 🎬 **감정 기반 영화 추천**: AI 모델을 활용한 감정 분석 기반 영화 추천
- 🔍 **영화 검색 기능**: 영화 제목으로 검색하여 원하는 영화를 빠르게 찾기
- 💬 **리뷰 및 댓글 시스템**: 영화에 대한 리뷰 작성 및 댓글 기능
- 👤 **프로필 관리**: 프로필 이미지, 닉네임, 찜한 영화 관리
- 🎨 **다크 테마 디자인**: 모던한 다크 테마 UI/UX
- 🎠 **카루셀 인터페이스**: 메인 페이지 및 인기 영화 카루셀

## 기술 스택

### Backend
- Django 5.2
- Django REST Framework
- Python 3.11
- SQLite
- Hugging Face Transformers (영화 감정 분석)

### Frontend
- Vue 3 (Composition API)
- Vue Router
- Pinia (상태 관리)
- Axios
- Bootstrap 5.3
- Vite
- 커스텀 폰트 (Suit, Paperozi 등)

## 프로젝트 구조

```
final-pjt-team7/
├── backend/                 # Django 프로젝트
│   ├── accounts/            # 사용자 인증 앱
│   │   ├── models.py        # User 모델 (AbstractUser 상속)
│   │   ├── views.py         # 인증 뷰 (회원가입, 로그인, 프로필)
│   │   ├── serializers.py   # 사용자 시리얼라이저
│   │   └── urls.py          # 인증 URL 라우팅
│   ├── movies/              # 영화 데이터 앱
│   │   ├── models.py        # Movie, Genre 모델
│   │   ├── views.py         # 영화 뷰
│   │   ├── serializers.py   # 영화 시리얼라이저
│   │   └── urls.py          # 영화 URL 라우팅
│   ├── community/           # 리뷰 및 댓글 앱
│   │   ├── models.py        # Review, Comment 모델
│   │   ├── views.py         # 리뷰/댓글 뷰셋
│   │   ├── serializers.py   # 리뷰/댓글 시리얼라이저
│   │   └── urls.py          # 리뷰/댓글 URL 라우팅
│   ├── moods/               # 영화 감정 분석 앱
│   │   ├── models.py        # MovieMood 모델
│   │   └── management/commands/movie_moods.py  # 영화 감정 분석 명령어
│   ├── recommends/          # 감정 기반 추천 앱
│   │   ├── models.py        # Recommendation 모델
│   │   ├── views.py         # 추천 뷰
│   │   ├── serializers.py   # 추천 시리얼라이저
│   │   └── urls.py          # 추천 URL 라우팅
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
│   │   │   ├── ReviewCreateView.vue
│   │   │   ├── ReviewDetailView.vue
│   │   │   ├── ReviewUpdateView.vue
│   │   │   ├── ProfileView.vue
│   │   │   ├── ProfileEditView.vue
│   │   │   ├── ProfileEmotionsView.vue
│   │   │   ├── ProfileReviewsView.vue
│   │   │   ├── ProfileDibsView.vue
│   │   │   ├── RecommendView.vue
│   │   │   └── SearchView.vue
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

5. 영화 데이터 수집 (필수)
```bash
python manage.py get_tmdb
```
이 명령어는 TMDB API에서 인기 영화 데이터를 가져와 DB에 저장합니다 (약 5-10분 소요).

6. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

7. 서버 실행
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
  - 프로필 이미지 기본값: `no-profile.png` (이미지 없을 때)
  - 메뉴 버튼: 회원정보 수정, 감정 분석 기록, 리뷰, 찜한 영화
- 회원정보 수정 페이지 (`/profile/edit`)
  - 닉네임, 프로필 이미지, 비밀번호 수정 가능
  - 이미지 미리보기 기능
  - FormData를 통한 파일 업로드
- 감정 분석 기록 페이지 (`/profile/emotions`)
  - 사용자의 감정 분석 기록 조회
- 리뷰 페이지 (`/profile/reviews`)
  - 사용자가 작성한 리뷰 목록 조회
- 찜한 영화 페이지 (`/profile/dibs`)
  - 사용자가 찜한 영화 목록 조회

### 3. 영화 데이터
- 인기 영화 목록 조회
- 영화 상세 정보 조회
- **영화 검색 기능**: 영화 제목으로 검색 (인기도순 정렬)
- TMDB API 연동
- 영화 감정 분석 데이터 저장 (MovieMood 모델)
- 영화 데이터 수집 명령어: `python manage.py get_tmdb` (TMDB에서 인기 영화 데이터 가져오기)

### 4. 감정 기반 영화 추천
- **감정 선택**: 사용자가 현재 기분 선택 (심심할 땐, 화날 땐, 슬플 땐, 행복할 땐, 긴장/스트레스)
- **AI 감정 분석**: Hugging Face `roberta-base-go_emotions` 모델을 사용한 영화 줄거리 감정 분석
- **추천 알고리즘**: 
  - 사용자 감정을 영화 감정 태그로 매핑
  - 감정에 맞는 영화 필터링
  - 인기도 순으로 상위 30개 선택 후 랜덤 4개 추천
- **추천 기록 저장**: 사용자별 추천 기록 저장 및 조회
- **관리 명령어**: `python manage.py movie_moods` (영화 감정 분석 실행)

### 5. 리뷰 및 댓글
- **리뷰 작성**: 로그인한 사용자만 작성 가능, 한 유저당 한 영화에 하나의 리뷰만 작성 가능
- **리뷰 조회**: 로그인 없이도 모든 리뷰 조회 가능
- **리뷰 수정/삭제**: 본인이 작성한 리뷰만 수정/삭제 가능
- **리뷰 상세 페이지**: 리뷰 내용, 좋아요, 댓글 확인 가능
- **리뷰 목록 페이지**: 영화별 리뷰 목록 조회 및 정렬
  - 정렬 필터: 최신순, 오래된순, 좋아요순, 평점 높은순, 평점 낮은순
- **리뷰 좋아요**: 로그인한 사용자만 좋아요 가능
- **댓글 기능**: 리뷰에 댓글 작성 및 삭제 (본인 댓글만 삭제 가능)
- **페이지네이션**: 리뷰 목록은 페이지네이션 적용 (페이지당 20개)
- **닉네임 표시**: 리뷰 및 댓글 작성자 닉네임 표시 (닉네임이 없으면 사용자명 표시)

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

### community 앱
- **community_review**: 리뷰 정보
  - user, movie, title, content, rank (1-5), created_at, updated_at
  - unique_together: (user, movie) - 한 유저당 한 영화에 하나의 리뷰만 작성 가능
- **community_comment**: 댓글 정보
  - review, user, content, created_at, updated_at
- **community_review_like_users**: 리뷰 좋아요 관계 (Many-to-Many)

### moods 앱
- **moods_moviemood**: 영화 감정 분석 결과
  - movie (OneToOne), dominant_mood, score_details (JSON), created_at
  - AI 모델을 통한 영화 줄거리 감정 분석 결과 저장

### recommends 앱
- **recommends_recommendation**: 추천 기록
  - user, mood, recommended_movies (Many-to-Many), created_at
  - 사용자별 감정 기반 추천 기록 저장

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
- `GET /api/v1/movies/?search=검색어` - 영화 검색 (제목으로 검색, 인기도순 정렬)
- `GET /api/v1/movies/{id}/` - 영화 상세 정보 조회 (tmdb_id 사용)
- `POST /api/v1/movies/{id}/likes/` - 영화 찜하기/취소 (인증 필요)
- `GET /api/v1/movies/my-likes/` - 내가 찜한 영화 목록 조회 (인증 필요)

### 리뷰 및 댓글 (community)
- `GET /api/v1/community/reviews/` - 리뷰 목록 조회 (인증 불필요)
  - 쿼리 파라미터: `movie={movie_id}` (DB의 id)
  - 페이지네이션: 페이지당 20개
- `POST /api/v1/community/reviews/` - 리뷰 작성 (인증 필요)
  - 요청: `{ title, content, rank (1-5), movie (DB의 id) }`
- `GET /api/v1/community/reviews/{id}/` - 리뷰 상세 조회 (인증 불필요)
- `PUT /api/v1/community/reviews/{id}/` - 리뷰 수정 (인증 필요, 본인만)
- `DELETE /api/v1/community/reviews/{id}/` - 리뷰 삭제 (인증 필요, 본인만)
- `POST /api/v1/community/reviews/{id}/likes/` - 리뷰 좋아요/취소 (인증 필요)
- `GET /api/v1/community/reviews/{id}/comments/` - 댓글 목록 조회 (인증 불필요)
- `POST /api/v1/community/reviews/{id}/comments/` - 댓글 작성 (인증 필요)
- `DELETE /api/v1/community/reviews/{id}/comments/{comment_id}/` - 댓글 삭제 (인증 필요, 본인만)

### 감정 기반 추천 (recommends)
- `POST /api/v1/recommends/generate/` - 감정 기반 영화 추천 생성 (인증 필요)
  - 요청: `{ mood: "bored" | "angry" | "sad" | "happy" | "stressed" }`
  - 응답: 추천 영화 목록 (4개)
- `GET /api/v1/recommends/history/` - 추천 기록 조회 (인증 필요)
  - 응답: 사용자별 추천 기록 목록

## 화면 구성

### 1. 메인 페이지 (/)
- 상단 프로모션 배너 카루셀 (TOP 5 영화)
  - "AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다" 메인 텍스트
  - "지금 바로 나만의 맞춤 영화를 만나보세요" 서브타이틀
  - "감정 다시 선택하기" 버튼
  - 텍스트는 한 줄로 표시되며 하단에 배치
- **검색창** (프로모션 배너 바로 아래)
  - 영화 제목 검색 (엔터 키로 검색)
  - 검색 결과 페이지로 이동 (`/search?q=검색어`)
  - 다크 테마 디자인 (빨간색 포커스 효과)
- 감정 선택 모달 (기분에 맞는 영화 추천)
- 인기 영화 TOP 10 카루셀
- 네비게이션 바 (SVG 로고, 홈, 로그인, 회원가입 버튼)
- 인기 영화 카드 클릭 시 영화 상세 페이지로 이동

### 2. 영화 검색 페이지 (/search)
- 검색어로 영화 검색 결과 표시
- 영화 포스터, 제목, 개봉년도 표시
- 검색 결과가 없을 때 안내 메시지
- 영화 카드 클릭 시 영화 상세 페이지로 이동

### 3. 로그인 페이지 (/login)
- 이메일과 비밀번호로 로그인 (이메일 기반 인증)
- JWT 토큰 기반 인증
- 로그인 성공 시 홈으로 리다이렉트
- 로그인 실패 시 에러 메시지 표시 (이메일/비밀번호 구분)
- 토큰 만료 시 자동 로그아웃 알림 팝업

### 4. 회원가입 페이지 (/register)
- 이름, 닉네임, 이메일, 비밀번호 입력
- 회원가입 성공 시 로그인 페이지로 리다이렉트

### 5. 영화 상세 페이지 (/movies/:id)
- Hero 섹션: 배경 이미지와 영화 정보 오버레이
- 영화 포스터, 제목, 장르, 개봉년도, TMDB 평점 표시
- 찜하기 버튼 (로그인한 사용자만)
- 후기 보기, 예고편 보기 버튼 (스크롤 이동)
- 줄거리 (overview) 표시
- 출연/제작진 섹션: 4열 2행 레이아웃 (8명 표시, 카루셀 지원)
- YouTube 예고편 섹션
- 리뷰 섹션 (상위 3개 미리보기, 최신순 정렬)
- 로그인한 사용자에게만 "리뷰 작성하기" 버튼 표시
- "전체보기 →" 버튼 클릭 시 해당 영화의 리뷰 페이지로 이동
- 리뷰 카드 클릭 시 리뷰 상세 페이지로 이동

### 6. 영화별 리뷰 페이지 (/movies/:id/reviews)
- 해당 영화의 모든 리뷰 조회 (로그인 없이도 조회 가능)
- 영화 정보 헤더 (제목, 리뷰 개수)
- 로그인한 사용자에게만 "리뷰 작성하기" 버튼 표시
- 리뷰 정렬 필터 (드롭다운):
  - 최신 순 (기본값)
  - 오래된 순
  - 좋아요 순
  - 높은 평가 순
  - 낮은 평가 순
- 리뷰 카드에 작성자 닉네임, 작성일, 평점, 좋아요 수, 댓글 수 표시
- 리뷰 카드 클릭 시 리뷰 상세 페이지로 이동
- 뒤로가기 버튼 (영화 상세 페이지로 이동)

### 7. 리뷰 작성 페이지 (/movies/:id/reviews/create)
- 리뷰 제목, 내용, 평점 (1-5점 라디오 버튼) 입력
- HTML5 폼 검증 (제목, 내용 필수)
- 중복 리뷰 작성 방지 (이미 작성한 경우 알림 표시)
- 등록 완료 시 영화별 리뷰 페이지로 이동

### 8. 리뷰 상세 페이지 (/movies/:id/reviews/:reviewId)
- 리뷰 상세 내용 표시 (제목, 내용, 평점, 작성자 닉네임)
- 로그인한 사용자만 좋아요 버튼 표시 (로그아웃 시 좋아요 개수만 표시)
- 댓글 목록 표시 (작성자 닉네임)
- 로그인한 사용자만 댓글 작성 가능 (로그아웃 시 로그인 안내 메시지)
- 본인이 작성한 리뷰만 수정/삭제 버튼 표시
- 본인이 작성한 댓글만 삭제 버튼 표시
- 뒤로가기 버튼 (영화별 리뷰 페이지로 이동)

### 9. 리뷰 수정 페이지 (/reviews/:reviewId/update)
- 기존 리뷰 내용 수정 (제목, 내용, 평점)
- 평점 선택을 라디오 버튼으로 제공 (1-5점)
- 수정 완료 시 리뷰 상세 페이지로 이동

### 10. 프로필 페이지 (/profile)
- 사용자 정보 표시 (프로필 이미지, 닉네임, 이메일, 가입일)
- 메뉴 버튼:
  - 회원정보 수정 → `/profile/edit`
  - 감정 분석 기록 → `/profile/emotions` (준비 중)
  - 리뷰 → `/profile/reviews` (준비 중)
- 뒤로가기 버튼 (메인 페이지로 이동)

### 11. 회원정보 수정 페이지 (/profile/edit)
- 닉네임 수정
- 프로필 이미지 업로드/수정 (미리보기 기능)
- 비밀번호 변경 (선택사항)
- 이메일 수정 불가 (보안 정책)
- 수정 완료 시 프로필 페이지로 자동 이동

### 12. 감정 분석 기록 페이지 (/profile/emotions)
- 준비 중 (다른 팀원이 구현 예정)

### 13. 리뷰 페이지 (/profile/reviews)
- 사용자가 작성한 리뷰 목록 조회
- 리뷰 카드 클릭 시 리뷰 상세 페이지로 이동
- 뒤로가기 버튼 (프로필 페이지로 이동)

### 14. 찜한 영화 페이지 (/profile/dibs)
- 사용자가 찜한 영화 목록 조회
- 영화 카드 클릭 시 영화 상세 페이지로 이동
- 뒤로가기 버튼 (프로필 페이지로 이동)

### 15. 감정 기반 추천 페이지 (/recommend)
- 감정 선택 및 영화 추천 결과 표시
- 추천된 영화 카드 클릭 시 영화 상세 페이지로 이동
- 뒤로가기 버튼 (메인 페이지로 이동)

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
- ✅ **리뷰 기능 완전 구현**:
  - 리뷰 작성, 수정, 삭제, 상세 조회 기능 완료
  - 리뷰 목록 페이지 및 정렬 기능
  - 한 유저당 한 영화에 하나의 리뷰만 작성 가능 (unique_together 제약)
  - 로그인 없이도 리뷰 조회 가능
  - 리뷰 작성 시 중복 체크 및 알림 기능
- ✅ **댓글 기능 구현**:
  - 리뷰에 댓글 작성 및 삭제 기능
  - 본인이 작성한 댓글만 삭제 가능
  - 로그인한 사용자만 댓글 작성 가능
- ✅ **좋아요 기능 구현**:
  - 리뷰 좋아요/좋아요 취소 기능
  - 로그인한 사용자만 좋아요 가능
  - 좋아요 버튼 스타일링 (핑크색 배경, 호버 효과)
- ✅ **UI/UX 개선**:
  - 리뷰 작성하기 버튼 (로그인 시에만 표시)
  - 평점 선택을 라디오 버튼으로 변경 (1-5점)
  - HTML5 폼 검증 적용
  - 닉네임 표시 기능 (리뷰 및 댓글 작성자)
  - 뒤로가기 버튼 라우팅 개선
  - YouTube 예고편 기능 추가
- ✅ **페이지네이션 설정**: 리뷰 목록 API에 페이지네이션 적용 (페이지당 20개)
- ✅ **인증 상태 확인**: 앱 시작 시 토큰 유효성 검증 및 자동 로그아웃 기능
- ✅ **감정 기반 영화 추천 알고리즘 구현**:
  - 사용자 감정(bored, angry, sad, happy, stressed) 기반 영화 추천
  - AI 모델을 통한 영화 감정 분석 (Hugging Face `roberta-base-go_emotions` 모델)
  - 감정 매핑 시스템 (사용자 감정 → 영화 감정 태그)
  - 인기도 기반 필터링 및 랜덤 추천 (상위 30개 중 4개 선택)
  - 추천 기록 저장 기능
  - 관리 명령어: `python manage.py movie_moods` (영화 감정 분석 실행)
- ✅ **UI/UX 대폭 개선**:
  - **다크 테마 디자인**: 전체 사이트에 다크 테마 적용
  - **로고 디자인**: SVG 기반 커브 로고로 변경 (Mood-Match)
  - **메인 페이지 카루셀**: 상단 프로모션 배너 및 인기 영화 TOP 10 카루셀 구현
    - 프로모션 배너에 "AI가 당신의 기분을 분석하여 완벽한 영화를 추천해드립니다" 텍스트 추가
    - 카루셀 콘텐츠 가로폭 확대 (800px → 1200px)
    - 텍스트 한 줄 표시 및 위치 조정
    - 텍스트 스타일 최적화 (폰트 크기, 굵기 조정)
  - **영화 검색 기능 구현**:
    - 검색창을 프로모션 배너 바로 아래로 배치
    - 검색 버튼 제거 (엔터 키로만 검색)
    - 검색 결과 페이지 (`/search`) 추가
    - 영화 제목으로 검색 (인기도순 정렬)
    - 검색창 다크 테마 디자인 (빨간색 포커스 효과)
    - 검색 결과가 없을 때 안내 메시지 표시
  - **감정 선택 모달**: 기분 선택 팝업창 디자인 개선 (X 버튼, 다크 테마)
  - **영화 상세 페이지 리디자인**: 스트리밍 서비스 스타일 적용
    - Hero 섹션 배경 이미지
    - 포스터와 줄거리 나란히 배치
    - 출연/제작진 4열 2행 레이아웃 (8개 표시)
    - 찜하기, 후기 보기, 예고편 보기 버튼
    - TMDB 평점 표시 (별 이모티콘 포함)
  - **리뷰 페이지 스타일 통일**: 모든 리뷰 관련 페이지에 일관된 카드 디자인 적용
  - **NavBar 개선**: 
    - SVG 로고 적용
    - 버튼 호버 효과 (다크 배경, 흰색 텍스트)
    - 현재 페이지 표시 (흰색 텍스트)
    - 버튼 스타일 통일
  - **뒤로가기 버튼**: 모든 페이지에 일관된 뒤로가기 버튼 추가
  - **프로필 이미지 기본값**: 프로필 이미지가 없을 때 `no-profile.png` 표시
  - **사용자 아바타 제거**: 리뷰 목록 및 상세 페이지에서 사용자 아바타 제거
  - **버튼 스타일 통일**: 회색 텍스트, 호버 효과, 테두리 제거
  - **로그인/회원가입 페이지**: X 버튼 추가 (메인 화면으로 이동)
  - **폰트 적용**: 커스텀 폰트 (Suit, Paperozi 등) 적용
- ✅ **네비게이션 개선**:
  - 리뷰 작성 페이지 → 리뷰 목록 페이지
  - 리뷰 목록 페이지 → 영화 상세 페이지
  - 프로필 리뷰 상세 → 영화 리뷰 목록 페이지 (뒤로가기)
- ✅ **추가 페이지 구현**:
  - `ProfileDibsView.vue`: 찜한 영화 목록 페이지
  - `RecommendView.vue`: 감정 기반 영화 추천 페이지
  - 모든 프로필 관련 페이지 스타일 통일

## 주의사항

1. **API 키 보안**: TMDB API 키는 `.env` 파일에 저장하고 절대 공개 저장소에 커밋하지 마세요.
2. **CORS 설정**: 프론트엔드와 백엔드가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.
3. **환경 변수**: `.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.
4. **가상환경**: 백엔드 개발 시 venv 가상환경 사용을 권장합니다.
5. **영화 데이터 수집**: 영화 데이터가 없으면 다음 명령어로 TMDB에서 데이터를 가져와야 합니다:
   ```bash
   python manage.py get_tmdb
   ```
   이 명령어는 TMDB API에서 인기 영화 데이터를 가져와 DB에 저장합니다 (약 5-10분 소요).

6. **영화 감정 분석**: 감정 기반 추천 기능을 사용하려면 먼저 영화 감정 분석을 실행해야 합니다:
   ```bash
   python manage.py movie_moods
   ```
   이 명령어는 `overview_en` 필드가 있는 영화들을 AI 모델로 분석하여 `MovieMood` 테이블에 저장합니다.
   분석되지 않은 영화가 많으면 추천 알고리즘이 인기도 기반 랜덤 추천으로 fallback됩니다.

## 참고 사이트

- [TMDB API](https://www.themoviedb.org/documentation/api)
- [왓챠피디아](https://pedia.watcha.com/ko-KR/)

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
