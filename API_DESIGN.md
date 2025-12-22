# API 설계 문서

## RESTful API 설계 원칙

이 프로젝트는 RESTful 원칙을 준수하여 설계되었습니다.

### URL 설계 원칙
- 리소스 중심의 URL 구조
- 계층적 관계 표현
- 동사 대신 명사 사용

### HTTP Method 사용
- `GET`: 데이터 조회 (Read)
- `POST`: 데이터 생성 (Create)
- `PUT/PATCH`: 데이터 수정 (Update)
- `DELETE`: 데이터 삭제 (Delete)

### Response Status Code
- `200 OK`: 성공적인 요청
- `201 Created`: 리소스 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스 없음
- `500 Internal Server Error`: 서버 오류

## API 엔드포인트

### 1. 인증 (Accounts)

#### 회원가입
```
POST /api/v1/accounts/register/
Request Body:
{
  "username": "user123",
  "email": "user@example.com",
  "nickname": "닉네임",
  "password": "password123",
  "password_confirm": "password123"
}
Response: 201 Created
{
  "user": {...},
  "tokens": {
    "access": "...",
    "refresh": "..."
  }
}
```

#### 로그인
```
POST /api/v1/accounts/login/
Request Body:
{
  "username": "user123",
  "password": "password123"
}
Response: 200 OK
{
  "user": {...},
  "tokens": {
    "access": "...",
    "refresh": "..."
  }
}
```

#### 프로필 조회
```
GET /api/v1/accounts/profile/
Headers: Authorization: Bearer {access_token}
Response: 200 OK
{
  "id": 1,
  "username": "user123",
  "email": "user@example.com",
  "nickname": "닉네임",
  ...
}
```

#### 프로필 수정
```
PUT /api/v1/accounts/profile/update/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "nickname": "새 닉네임",
  "email": "new@example.com"
}
Response: 200 OK
```

#### 토큰 갱신
```
POST /api/v1/accounts/token/refresh/
Request Body:
{
  "refresh": "{refresh_token}"
}
Response: 200 OK
{
  "access": "..."
}
```

### 2. 영화 (Movies)

#### 영화 목록 조회
```
GET /api/v1/movies/?page=1&ordering=-popularity
Response: 200 OK
{
  "count": 100,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

#### 영화 상세 조회
```
GET /api/v1/movies/{id}/
Response: 200 OK
{
  "id": 1,
  "tmdb_id": 12345,
  "title": "영화 제목",
  "overview": "줄거리",
  "genres": [...],
  "cast": [...],
  "crew": [...],
  "videos": [...],
  "is_wishlisted": false,
  ...
}
```

#### 인기 영화
```
GET /api/v1/movies/popular/
Response: 200 OK
[...]
```

#### 영화 검색
```
GET /api/v1/movies/search/?q=검색어
Response: 200 OK
[...]
```

#### 위시리스트 추가
```
POST /api/v1/movies/{id}/wishlist/
Headers: Authorization: Bearer {access_token}
Response: 201 Created
{
  "message": "위시리스트에 추가되었습니다."
}
```

#### 위시리스트 제거
```
DELETE /api/v1/movies/{id}/wishlist/
Headers: Authorization: Bearer {access_token}
Response: 200 OK
{
  "message": "위시리스트에서 제거되었습니다."
}
```

#### TMDB 동기화
```
POST /api/v1/movies/sync/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "tmdb_id": 12345
}
Response: 201 Created
{...}
```

### 3. 리뷰 (Reviews)

#### 리뷰 목록
```
GET /api/v1/reviews/?movie={movie_id}&user={user_id}
Response: 200 OK
{
  "count": 50,
  "results": [...]
}
```

#### 리뷰 작성
```
POST /api/v1/reviews/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "movie": 1,
  "title": "리뷰 제목",
  "content": "리뷰 내용",
  "rating": 5
}
Response: 201 Created
{...}
```

#### 리뷰 수정
```
PUT /api/v1/reviews/{id}/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "title": "수정된 제목",
  "content": "수정된 내용",
  "rating": 4
}
Response: 200 OK
{...}
```

#### 리뷰 삭제
```
DELETE /api/v1/reviews/{id}/
Headers: Authorization: Bearer {access_token}
Response: 204 No Content
```

#### 리뷰 좋아요
```
POST /api/v1/reviews/{id}/like/
Headers: Authorization: Bearer {access_token}
Response: 201 Created
{
  "message": "좋아요를 눌렀습니다."
}
```

#### 리뷰 좋아요 취소
```
DELETE /api/v1/reviews/{id}/like/
Headers: Authorization: Bearer {access_token}
Response: 200 OK
{
  "message": "좋아요를 취소했습니다."
}
```

#### 리뷰 댓글 작성
```
POST /api/v1/reviews/{id}/comments/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "content": "댓글 내용"
}
Response: 201 Created
{...}
```

### 4. 추천 (Recommendations)

#### 감정 목록
```
GET /api/v1/recommendations/emotions/
Response: 200 OK
[
  {
    "id": 1,
    "name": "happy",
    "description": "행복하고 즐거운 감정"
  },
  ...
]
```

#### 추천 생성
```
POST /api/v1/recommendations/generate/
Headers: Authorization: Bearer {access_token}
Request Body:
{
  "emotion_id": 1
}
Response: 201 Created
[
  {
    "id": 1,
    "emotion": {...},
    "movie": {...},
    "created_at": "..."
  },
  ...
]
```

#### 추천 기록 조회
```
GET /api/v1/recommendations/history/?emotion_id={emotion_id}
Headers: Authorization: Bearer {access_token}
Response: 200 OK
[...]
```

#### 사용자 감정 기록
```
GET /api/v1/recommendations/user-emotions/
Headers: Authorization: Bearer {access_token}
Response: 200 OK
{
  "count": 10,
  "results": [...]
}
```

## 데이터 관계

### URL 구조로 표현된 관계
- `/api/v1/movies/{movie_id}/wishlist/` - 영화와 사용자의 위시리스트 관계
- `/api/v1/reviews/?movie={movie_id}` - 영화와 리뷰의 관계
- `/api/v1/reviews/{review_id}/like/` - 리뷰와 사용자의 좋아요 관계
- `/api/v1/reviews/{review_id}/comments/` - 리뷰와 댓글의 관계
- `/api/v1/recommendations/history/?emotion_id={emotion_id}` - 감정과 추천의 관계

### HTTP Method와 데이터베이스 변화
- `POST`: 데이터베이스에 새 레코드 생성
- `PUT/PATCH`: 기존 레코드 수정
- `DELETE`: 레코드 삭제
- `GET`: 데이터 조회 (변화 없음)

## 인증 및 권한

### JWT 토큰 기반 인증
- Access Token: 1시간 유효
- Refresh Token: 7일 유효
- Authorization 헤더에 Bearer 토큰 포함

### 권한 레벨
- `AllowAny`: 인증 불필요
- `IsAuthenticatedOrReadOnly`: 읽기는 인증 불필요, 쓰기는 인증 필요
- `IsAuthenticated`: 모든 작업에 인증 필요

## 에러 처리

### 표준 에러 응답 형식
```json
{
  "error": "에러 메시지",
  "detail": "상세 정보"
}
```

### 상태 코드별 에러
- `400`: 요청 데이터 검증 실패
- `401`: 인증 토큰 없음 또는 만료
- `403`: 권한 없음
- `404`: 리소스 없음
- `500`: 서버 내부 오류

