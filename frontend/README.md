# Frontend (Vue 3 SPA)

## 기술 스택

- Vue 3 (Composition API)
- Vue Router
- Pinia (상태 관리)
- Axios (HTTP 클라이언트)
- Bootstrap 5.3
- Vite (빌드 도구)

## 프로젝트 구조

```
frontend/
├── src/
│   ├── components/          # 재사용 가능한 컴포넌트
│   │   └── NavBar.vue        # 네비게이션 바
│   ├── views/                # 페이지 뷰 컴포넌트
│   │   ├── HomeView.vue      # 메인 페이지 (인기 영화 목록)
│   │   ├── LoginView.vue     # 로그인 페이지
│   │   ├── RegisterView.vue  # 회원가입 페이지
│   │   ├── MovieDetailView.vue    # 영화 상세 페이지
│   │   └── MovieReviewsView.vue   # 영화별 리뷰 페이지
│   ├── router/               # 라우터 설정
│   │   └── index.js
│   ├── stores/               # Pinia 스토어
│   │   └── auth.js           # 인증 상태 관리
│   ├── api/                  # API 클라이언트
│   │   └── index.js          # Axios 인스턴스 및 인터셉터
│   ├── data/                 # Mock 데이터
│   │   └── mockData.js       # 모킹 API 함수들
│   └── main.js               # 앱 진입점
└── package.json
```

## 설치 및 실행

1. 의존성 설치
```bash
npm install
```

2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

3. 개발 서버 실행
```bash
npm run dev
```

서버는 http://localhost:5173 에서 실행됩니다.

## 주요 기능

### 페이지 구성
- **홈 페이지 (/)**: 인기 영화 카드 표시
- **로그인 페이지 (/login)**: 이메일과 비밀번호로 로그인 (이메일 기반 인증)
- **회원가입 페이지 (/register)**: 사용자 등록 (이름, 닉네임, 이메일, 비밀번호)
- **영화 상세 페이지 (/movies/:id)**: 영화 정보 및 리뷰 미리보기
- **영화별 리뷰 페이지 (/movies/:id/reviews)**: 해당 영화의 모든 리뷰 조회 및 정렬

### 인증 기능
- 이메일 기반 로그인
- JWT 토큰 기반 인증 (Access Token, Refresh Token)
- 자동 토큰 갱신 (API 인터셉터)
- 로그아웃 기능 (NavBar)
- 로그인 상태에 따른 UI 변경 (로그인/회원가입 버튼 ↔ 로그아웃 버튼)

### 리뷰 기능
- 리뷰 목록 조회 (영화별 필터링)
- 리뷰 정렬 필터:
  - 최신 순 (기본값)
  - 오래된 순
  - 좋아요 순
  - 높은 평가 순
  - 낮은 평가 순
- 리뷰 좋아요 기능

## 빌드

프로덕션 빌드:
```bash
npm run build
```

빌드된 파일은 `dist/` 디렉토리에 생성됩니다.

## 최근 업데이트 내역

### 2024년 업데이트
- ✅ **로그인 시스템**: 이메일 기반 로그인으로 변경
- ✅ **로그아웃 기능**: NavBar에 로그아웃 버튼 추가
- ✅ **API 인터셉터 개선**: 로그인/회원가입 API는 인터셉터에서 제외하여 리다이렉트 문제 해결
- ✅ **에러 처리**: 로그인 실패 시 리다이렉트 없이 에러 메시지만 표시

## 개발 모드

현재는 Mock 데이터를 사용하여 개발 중입니다. `src/data/mockData.js`의 `mockApi`를 통해 API를 모킹하고 있습니다.

실제 백엔드 API를 사용하려면:
1. 백엔드 서버가 실행 중이어야 합니다
2. `src/data/mockData.js`의 모킹 함수를 실제 API 호출로 대체하거나
3. `src/api/index.js`의 axios 인스턴스를 직접 사용하세요

## API 클라이언트

`src/api/index.js`에서 axios 인스턴스를 설정하고 있습니다:
- Request Interceptor: JWT 토큰 자동 추가
- Response Interceptor: 401 에러 시 토큰 갱신 시도, 실패 시 로그인 페이지로 리다이렉트
- 로그인/회원가입 API는 인터셉터에서 제외되어 리다이렉트 문제가 해결되었습니다

