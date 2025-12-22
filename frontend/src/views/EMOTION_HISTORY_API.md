# 감정 기록 페이지 API 구조

## 필요한 백엔드 API 엔드포인트

### 1. 감정 분석 통계
```
GET /api/v1/recommendations/user-emotions/statistics/
```

**응답 형식:**
```json
{
  "happy": 3,
  "romantic": 4,
  "calm": 2,
  "sad": 1,
  "excited": 0,
  "angry": 0,
  "anxious": 0,
  "thrilled": 0
}
```

### 2. 사용자 감정 기록
```
GET /api/v1/recommendations/user-emotions/
```

**응답 형식:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "emotion": {
        "id": 1,
        "name": "happy",
        "description": "행복"
      },
      "created_at": "2024-03-15T14:30:00Z",
      "recommended_movies": [
        {
          "id": 5,
          "tmdb_id": 13,
          "title": "포레스트 검프",
          "poster_path": "...",
          "vote_average": 8.8
        }
      ]
    },
    {
      "id": 2,
      "emotion": {
        "id": 7,
        "name": "romantic",
        "description": "로맨틱"
      },
      "created_at": "2024-03-10T20:15:00Z",
      "recommended_movies": [
        {
          "id": 4,
          "tmdb_id": 313369,
          "title": "라라랜드",
          "poster_path": "...",
          "vote_average": 8.2
        }
      ]
    }
  ]
}
```

## 데이터 구조 요구사항

### UserEmotion 모델
- `id`: 감정 기록 ID
- `emotion`: 감정 객체 (id, name, description 포함)
- `created_at`: 생성 날짜/시간 (ISO 8601 형식)
- `recommended_movies`: 추천된 영화 배열 (최소한 id, title, poster_path 포함)

### 감정 통계
- 각 감정별 총 사용 횟수를 반환
- 감정 이름을 key로 하는 객체 형태

## 프론트엔드 연동 방법

`EmotionHistoryView.vue`에서 `MOCK_MODE`를 `false`로 변경하면 실제 API를 호출합니다:

```javascript
const MOCK_MODE = false  // 모킹 모드 비활성화
```

