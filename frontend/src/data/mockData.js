// 고정 데이터 (백엔드 통신 없이 사용)

export const mockMovies = [
  {
    id: 1,
    tmdb_id: 550,
    title: '파이트 클럽',
    original_title: 'Fight Club',
    poster_path: 'https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg',
    popularity: 85.5
  },
  {
    id: 2,
    tmdb_id: 238,
    title: '대부',
    original_title: 'The Godfather',
    poster_path: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    popularity: 120.3
  },
  {
    id: 3,
    tmdb_id: 424,
    title: '쇼생크 탈출',
    original_title: 'The Shawshank Redemption',
    poster_path: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    popularity: 95.8
  },
  {
    id: 4,
    tmdb_id: 13,
    title: '포레스트 검프',
    original_title: 'Forrest Gump',
    poster_path: 'https://image.tmdb.org/t/p/w500/arw2vcBve0OVe8x3l8KX0xXzJ8P.jpg',
    popularity: 92.5
  },
  {
    id: 5,
    tmdb_id: 155,
    title: '다크 나이트',
    original_title: 'The Dark Knight',
    poster_path: 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
    popularity: 110.2
  },
  {
    id: 6,
    tmdb_id: 27205,
    title: '인셉션',
    original_title: 'Inception',
    poster_path: 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg',
    popularity: 105.8
  },
  {
    id: 7,
    tmdb_id: 122,
    title: '반지의 제왕: 반지 원정대',
    original_title: 'The Lord of the Rings: The Fellowship of the Ring',
    poster_path: 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTM6bn6j3uGd3v56s.jpg',
    popularity: 98.5
  },
  {
    id: 8,
    tmdb_id: 278,
    title: '쇼생크 탈출',
    original_title: 'The Shawshank Redemption',
    poster_path: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    popularity: 88.2
  }
]

// API 모킹 함수들
export const mockApi = {
  // 지연 시뮬레이션
  delay: (ms = 500) => new Promise(resolve => setTimeout(resolve, ms)),

  // 인기 영화
  getPopularMovies: async () => {
    await mockApi.delay()
    return { data: mockMovies.slice(0, 8) }
  },

  // 영화 상세 정보
  getMovieDetail: async (id) => {
    await mockApi.delay()
    const movie = mockMovies.find(m => m.id === parseInt(id))
    if (movie) {
      // 기본 정보에 추가 필드 포함
      return { 
        data: {
          ...movie,
          overview: '영화 상세 정보입니다.',
          release_date: '1999-01-01',
          vote_average: 8.5,
          vote_count: 1000
        } 
      }
    }
    return { data: null }
  },

  // 리뷰 목록 (영화 ID로 필터링 가능)
  getReviews: async (params = {}) => {
    await mockApi.delay()
    // 더미 리뷰 데이터 (더 다양한 데이터 추가)
    const mockReviews = [
      {
        id: 1,
        user: { id: 1, nickname: 'user1' },
        movie: 1,
        movie_title: '파이트 클럽',
        title: '정말 인상적인 영화',
        content: '이 영화는 정말 놀라웠습니다. 스토리와 연출이 완벽합니다.',
        rating: 5,
        like_count: 15,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-10T10:00:00Z'
      },
      {
        id: 2,
        user: { id: 2, nickname: 'user2' },
        movie: 1,
        movie_title: '파이트 클럽',
        title: '다시 보고 싶은 영화',
        content: '여러 번 봐도 재미있는 영화입니다.',
        rating: 4,
        like_count: 8,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-12T14:30:00Z'
      },
      {
        id: 3,
        user: { id: 3, nickname: 'user3' },
        movie: 1,
        movie_title: '파이트 클럽',
        title: '평범한 영화',
        content: '기대했던 것보다는 아쉬웠습니다.',
        rating: 2,
        like_count: 3,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-08T09:00:00Z'
      },
      {
        id: 4,
        user: { id: 4, nickname: 'user4' },
        movie: 1,
        movie_title: '파이트 클럽',
        title: '최고의 영화',
        content: '인생 영화입니다. 강력 추천합니다!',
        rating: 5,
        like_count: 25,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-15T16:20:00Z'
      },
      {
        id: 5,
        user: { id: 5, nickname: 'user5' },
        movie: 1,
        movie_title: '파이트 클럽',
        title: '재미있었어요',
        content: '스토리가 흥미롭고 연출도 좋았습니다.',
        rating: 4,
        like_count: 12,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-11T11:30:00Z'
      },
      {
        id: 6,
        user: { id: 3, nickname: 'user3' },
        movie: 2,
        movie_title: '대부',
        title: '클래식의 대명사',
        content: '마피아 영화의 교과서라고 할 수 있는 작품입니다.',
        rating: 5,
        like_count: 23,
        is_liked: false,
        comments: [],
        comments_count: 0,
        created_at: '2024-01-14T09:15:00Z'
      }
    ]

    let reviews = [...mockReviews]
    
    // 영화 ID로 필터링
    if (params.movie) {
      reviews = reviews.filter(r => r.movie === parseInt(params.movie))
    }
    
    // 정렬 처리
    if (params.ordering) {
      const orderField = params.ordering.startsWith('-') 
        ? params.ordering.substring(1) 
        : params.ordering
      const isDesc = params.ordering.startsWith('-')
      
      reviews.sort((a, b) => {
        let aVal, bVal
        
        switch (orderField) {
          case 'like_count':
            aVal = a.like_count
            bVal = b.like_count
            break
          case 'rating':
            aVal = a.rating
            bVal = b.rating
            break
          case 'created_at':
            aVal = new Date(a.created_at).getTime()
            bVal = new Date(b.created_at).getTime()
            break
          default:
            return 0
        }
        
        if (isDesc) {
          return bVal - aVal
        } else {
          return aVal - bVal
        }
      })
    }
    
    return { data: { results: reviews, count: reviews.length } }
  }
}

