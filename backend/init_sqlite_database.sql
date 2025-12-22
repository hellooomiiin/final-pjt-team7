-- SQLite 데이터베이스 초기화 스크립트
-- DDL: 테이블 생성
-- DML: 더미 데이터 삽입 (각 테이블당 20개씩)

-- Foreign Key 제약조건 활성화 (SQLite는 기본적으로 비활성화)
PRAGMA foreign_keys = ON;

-- ============================================
-- 1. USERS 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    nickname VARCHAR(100) NOT NULL
);

-- USERS 더미 데이터 20개
INSERT INTO users (email, nickname) VALUES
('user1@example.com', '영화마니아'),
('user2@example.com', '시네필'),
('user3@example.com', '무비러버'),
('user4@example.com', '영화좋아'),
('user5@example.com', '영화애호가'),
('user6@example.com', '시네마니아'),
('user7@example.com', '무비매니아'),
('user8@example.com', '영화광'),
('user9@example.com', '시네팬'),
('user10@example.com', '무비팬'),
('user11@example.com', '영화팬'),
('user12@example.com', '시네마팬'),
('user13@example.com', '무비좋아'),
('user14@example.com', '영화사랑'),
('user15@example.com', '시네사랑'),
('user16@example.com', '무비사랑'),
('user17@example.com', '영화덕후'),
('user18@example.com', '시네덕후'),
('user19@example.com', '무비덕후'),
('user20@example.com', '영화덕');

-- ============================================
-- 2. MOVIES 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    overview TEXT,
    poster_path VARCHAR(500),
    release_date DATE
);

-- MOVIES 더미 데이터 20개
INSERT INTO movies (title, overview, poster_path, release_date) VALUES
('인터스텔라', '지구의 미래를 구하기 위해 우주로 떠나는 한 팀의 탐험대 이야기', '/poster/interstellar.jpg', '2014-11-06'),
('인셉션', '꿈 속으로 들어가 생각을 훔치는 특수요원들의 이야기', '/poster/inception.jpg', '2010-07-21'),
('다크 나이트', '배트맨과 조커의 치열한 대결', '/poster/darkknight.jpg', '2008-07-18'),
('포레스트 검프', 'IQ 75의 남자가 겪는 특별한 인생 이야기', '/poster/forrest.jpg', '1994-07-06'),
('쇼생크 탈출', '감옥에서 희망을 잃지 않고 탈출을 꿈꾸는 두 남자의 이야기', '/poster/shawshank.jpg', '1994-09-23'),
('대부', '코를레오네 가문의 마피아 조직 이야기', '/poster/godfather.jpg', '1972-03-24'),
('파이트 클럽', '불면증에 시달리는 회사원과 비밀 결사의 만남', '/poster/fightclub.jpg', '1999-10-15'),
('라이언 일병 구하기', '노르망디 상륙 작전 후 한 병사를 찾아 나선 특수부대', '/poster/savingryan.jpg', '1998-07-24'),
('그린 마일', '사형수 교도소에서 일어나는 기적의 이야기', '/poster/greenmile.jpg', '1999-12-10'),
('펄프 픽션', '교차되는 여러 인물들의 이야기를 그린 영화', '/poster/pulpfiction.jpg', '1994-09-23'),
('매트릭스', '가상 현실과 실제 세계의 경계를 그린 SF 액션', '/poster/matrix.jpg', '1999-03-31'),
('글래디에이터', '로마 제국을 향한 한 용사의 복수 이야기', '/poster/gladiator.jpg', '2000-05-05'),
('타이타닉', '운명적인 사랑과 비극적 침몰의 이야기', '/poster/titanic.jpg', '1997-12-19'),
('아바타', '판도라 행성에서 펼쳐지는 판타지 SF 모험', '/poster/avatar.jpg', '2009-12-18'),
('어벤져스', '세계 최강의 슈퍼히어로들이 모인 팀의 활약', '/poster/avengers.jpg', '2012-05-04'),
('인피니티 워', '타노스와 어벤져스의 운명적 대결', '/poster/infinitywar.jpg', '2018-04-27'),
('엔드게임', '역사상 가장 위대한 최종 결전', '/poster/endgame.jpg', '2019-04-26'),
('라라랜드', '로스앤젤레스를 배경으로 한 뮤지컬 로맨스', '/poster/lalaland.jpg', '2016-12-16'),
('보헤미안 랩소디', '퀸의 전설적인 보컬 프레디 머큐리의 일대기', '/poster/bohemian.jpg', '2018-10-31'),
('죽은 시인의 사회', '전통과 규율을 가르치는 명문 학교의 새로운 교사', '/poster/deadpoets.jpg', '1989-06-02');

-- ============================================
-- 3. GENRES 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- GENRES 더미 데이터 20개
INSERT INTO genres (name) VALUES
('액션'),
('드라마'),
('SF'),
('스릴러'),
('공포'),
('코미디'),
('로맨스'),
('판타지'),
('범죄'),
('전쟁'),
('서부'),
('뮤지컬'),
('애니메이션'),
('다큐멘터리'),
('가족'),
('역사'),
('모험'),
('미스터리'),
('공상과학'),
('음악');

-- ============================================
-- 4. MOVIE_GENRES 테이블 생성 (N:M 관계)
-- ============================================
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- MOVIE_GENRES 더미 데이터 (각 영화당 1-3개 장르 연결)
INSERT INTO movie_genres (movie_id, genre_id) VALUES
-- 인터스텔라: SF, 드라마, 모험
(1, 3), (1, 2), (1, 17),
-- 인셉션: 액션, SF, 스릴러
(2, 1), (2, 3), (2, 4),
-- 다크 나이트: 액션, 범죄, 드라마
(3, 1), (3, 9), (3, 2),
-- 포레스트 검프: 드라마, 로맨스
(4, 2), (4, 7),
-- 쇼생크 탈출: 드라마
(5, 2),
-- 대부: 범죄, 드라마
(6, 9), (6, 2),
-- 파이트 클럽: 드라마, 스릴러
(7, 2), (7, 4),
-- 라이언 일병 구하기: 전쟁, 드라마, 액션
(8, 10), (8, 2), (8, 1),
-- 그린 마일: 드라마, 판타지
(9, 2), (9, 8),
-- 펄프 픽션: 범죄, 드라마
(10, 9), (10, 2),
-- 매트릭스: 액션, SF
(11, 1), (11, 3),
-- 글래디에이터: 액션, 드라마, 역사
(12, 1), (12, 2), (12, 16),
-- 타이타닉: 드라마, 로맨스
(13, 2), (13, 7),
-- 아바타: 액션, SF, 모험
(14, 1), (14, 3), (14, 17),
-- 어벤져스: 액션, SF, 모험
(15, 1), (15, 3), (15, 17),
-- 인피니티 워: 액션, SF, 모험
(16, 1), (16, 3), (16, 17),
-- 엔드게임: 액션, SF, 드라마
(17, 1), (17, 3), (17, 2),
-- 라라랜드: 뮤지컬, 로맨스, 드라마
(18, 12), (18, 7), (18, 2),
-- 보헤미안 랩소디: 드라마, 음악
(19, 2), (19, 20),
-- 죽은 시인의 사회: 드라마
(20, 2);

-- ============================================
-- 5. REVIEWS 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    rating REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);

-- REVIEWS 더미 데이터 20개
INSERT INTO reviews (user_id, movie_id, content, rating) VALUES
(1, 1, '인터스텔라는 정말 감동적인 작품입니다. 시간과 공간을 넘나드는 스토리가 인상적이에요.', 5.0),
(2, 2, '인셉션은 뇌를 자극하는 영화입니다. 여러 번 봐도 새로운 것을 발견하는 재미가 있어요.', 4.5),
(3, 3, '다크 나이트는 최고의 슈퍼히어로 영화입니다. 조커의 연기가 압권이에요.', 5.0),
(4, 4, '포레스트 검프는 삶에 대한 깊은 생각을 하게 만드는 영화입니다.', 4.8),
(5, 5, '쇼생크 탈출은 희망에 대한 메시지가 강렬한 작품입니다.', 5.0),
(6, 6, '대부는 마피아 영화의 클래식입니다. 영화사에 한 획을 그은 작품이에요.', 4.9),
(7, 7, '파이트 클럽은 충격적이고 생각할 거리를 주는 영화입니다.', 4.7),
(8, 8, '라이언 일병 구하기는 전쟁의 참혹함을 생생하게 보여주는 작품입니다.', 4.6),
(9, 9, '그린 마일은 눈물 없이는 볼 수 없는 감동적인 영화입니다.', 4.8),
(10, 10, '펄프 픽션은 독특한 구성과 스타일이 인상적인 작품입니다.', 4.5),
(11, 11, '매트릭스는 SF 영화의 새로운 지평을 연 작품입니다.', 4.9),
(12, 12, '글래디에이터는 액션과 드라마가 완벽하게 어우러진 영화입니다.', 4.7),
(13, 13, '타이타닉은 사랑과 비극이 공존하는 걸작입니다.', 4.6),
(14, 14, '아바타는 시각적 효과가 놀라운 영화입니다. 3D로 보면 더욱 좋아요.', 4.5),
(15, 15, '어벤져스는 모든 히어로가 한 자리에 모인 화려한 액션 영화입니다.', 4.8),
(16, 16, '인피니티 워는 긴장감 넘치는 스토리로 몰입도를 높였어요.', 4.7),
(17, 17, '엔드게임은 시리즈의 완벽한 마무리였습니다. 감동적이고 멋진 결말이에요.', 5.0),
(18, 18, '라라랜드는 음악과 춤이 아름다운 뮤지컬 영화입니다.', 4.6),
(19, 19, '보헤미안 랩소디는 퀸의 음악과 함께하는 감동적인 바이오그래피입니다.', 4.8),
(20, 20, '죽은 시인의 사회는 교육과 꿈에 대한 깊은 메시지를 전달합니다.', 4.7);

-- ============================================
-- 6. MOOD_LOGS 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS mood_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_input TEXT NOT NULL,
    input_embedding TEXT,
    detected_emotion VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- MOOD_LOGS 더미 데이터 20개
INSERT INTO mood_logs (user_id, user_input, input_embedding, detected_emotion, created_at) VALUES
(1, '오늘 정말 행복한 하루였어요! 좋은 일이 많이 생겼습니다.', NULL, 'happy', '2024-03-15 14:30:00'),
(2, '설레는 마음으로 하루를 시작했어요. 기대되는 일이 있어요.', NULL, 'excited', '2024-03-15 10:20:00'),
(3, '요즘 무슨 일이든 하기 싫고 우울한 기분이에요.', NULL, 'depressed', '2024-03-14 18:45:00'),
(4, '정말 화가 나요! 이런 일이 있을 줄 몰랐어요.', NULL, 'angry', '2024-03-14 16:15:00'),
(5, '시험 앞두고 긴장돼요. 잘 해낼 수 있을까 걱정이에요.', NULL, 'anxious', '2024-03-13 20:00:00'),
(6, '할 일이 없어서 심심해요. 재미있는 게 뭐가 있을까요?', NULL, 'bored', '2024-03-13 15:30:00'),
(7, '슬픈 일이 있어서 기분이 안 좋아요.', NULL, 'sad', '2024-03-12 22:10:00'),
(8, '새로운 것을 경험하고 싶어요. 무언가 새로운 시도를 해볼까 해요.', NULL, 'new', '2024-03-12 11:20:00'),
(9, '친구들과 함께 있어서 정말 행복해요!', NULL, 'happy', '2024-03-11 19:45:00'),
(10, '데이트가 기대돼요. 설레는 마음이에요.', NULL, 'excited', '2024-03-11 17:30:00'),
(11, '비가 오는 날씨가 우울하게 만들어요.', NULL, 'depressed', '2024-03-10 14:20:00'),
(12, '너무 화가 나서 차분해질 수가 없어요.', NULL, 'angry', '2024-03-10 09:15:00'),
(13, '면접이 있어서 긴장이 많이 되네요.', NULL, 'anxious', '2024-03-09 21:00:00'),
(14, '시간이 너무 느리게 가는 것 같아요. 심심해요.', NULL, 'bored', '2024-03-09 13:45:00'),
(15, '이별 후 슬픈 마음을 감출 수가 없어요.', NULL, 'sad', '2024-03-08 23:30:00'),
(16, '새로운 취미를 시작하고 싶어요. 무언가 새로운 도전이 필요해요.', NULL, 'new', '2024-03-08 10:10:00'),
(17, '좋은 소식을 들어서 정말 기뻐요!', NULL, 'happy', '2024-03-07 16:40:00'),
(18, '여행을 떠나는 게 너무 설레요!', NULL, 'excited', '2024-03-07 08:25:00'),
(19, '힘든 일들이 겹쳐서 우울한 기분이에요.', NULL, 'depressed', '2024-03-06 19:50:00'),
(20, '불공평한 일에 화가 나요.', NULL, 'angry', '2024-03-06 12:35:00');

-- ============================================
-- 7. MOVIE_SENTIMENTS 테이블 생성
-- ============================================
CREATE TABLE IF NOT EXISTS movie_sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    embedding TEXT,
    dominant_emotion VARCHAR(50),
    emotion_scores TEXT,  -- SQLite에서는 JSON을 TEXT로 저장
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);

-- MOVIE_SENTIMENTS 더미 데이터 20개 (JSON은 TEXT로 저장)
INSERT INTO movie_sentiments (movie_id, embedding, dominant_emotion, emotion_scores) VALUES
(1, NULL, 'excited', '{"happy": 0.1, "excited": 0.8, "depressed": 0.0, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(2, NULL, 'excited', '{"happy": 0.1, "excited": 0.7, "depressed": 0.0, "angry": 0.05, "anxious": 0.1, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(3, NULL, 'excited', '{"happy": 0.05, "excited": 0.75, "depressed": 0.0, "angry": 0.15, "anxious": 0.05, "bored": 0.0, "sad": 0.0, "new": 0.0}'),
(4, NULL, 'happy', '{"happy": 0.7, "excited": 0.1, "depressed": 0.05, "angry": 0.0, "anxious": 0.0, "bored": 0.0, "sad": 0.15, "new": 0.0}'),
(5, NULL, 'happy', '{"happy": 0.6, "excited": 0.05, "depressed": 0.1, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.2, "new": 0.0}'),
(6, NULL, 'angry', '{"happy": 0.05, "excited": 0.1, "depressed": 0.1, "angry": 0.6, "anxious": 0.1, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(7, NULL, 'angry', '{"happy": 0.1, "excited": 0.15, "depressed": 0.1, "angry": 0.5, "anxious": 0.1, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(8, NULL, 'anxious', '{"happy": 0.05, "excited": 0.1, "depressed": 0.15, "angry": 0.1, "anxious": 0.55, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(9, NULL, 'sad', '{"happy": 0.2, "excited": 0.05, "depressed": 0.15, "angry": 0.0, "anxious": 0.0, "bored": 0.0, "sad": 0.6, "new": 0.0}'),
(10, NULL, 'excited', '{"happy": 0.2, "excited": 0.65, "depressed": 0.0, "angry": 0.1, "anxious": 0.05, "bored": 0.0, "sad": 0.0, "new": 0.0}'),
(11, NULL, 'excited', '{"happy": 0.1, "excited": 0.8, "depressed": 0.0, "angry": 0.05, "anxious": 0.05, "bored": 0.0, "sad": 0.0, "new": 0.0}'),
(12, NULL, 'excited', '{"happy": 0.1, "excited": 0.7, "depressed": 0.0, "angry": 0.15, "anxious": 0.05, "bored": 0.0, "sad": 0.0, "new": 0.0}'),
(13, NULL, 'sad', '{"happy": 0.15, "excited": 0.1, "depressed": 0.1, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.6, "new": 0.0}'),
(14, NULL, 'excited', '{"happy": 0.15, "excited": 0.75, "depressed": 0.0, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(15, NULL, 'excited', '{"happy": 0.15, "excited": 0.8, "depressed": 0.0, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.0, "new": 0.0}'),
(16, NULL, 'sad', '{"happy": 0.05, "excited": 0.2, "depressed": 0.1, "angry": 0.1, "anxious": 0.1, "bored": 0.0, "sad": 0.45, "new": 0.0}'),
(17, NULL, 'happy', '{"happy": 0.65, "excited": 0.25, "depressed": 0.0, "angry": 0.0, "anxious": 0.05, "bored": 0.0, "sad": 0.05, "new": 0.0}'),
(18, NULL, 'happy', '{"happy": 0.7, "excited": 0.2, "depressed": 0.0, "angry": 0.0, "anxious": 0.0, "bored": 0.0, "sad": 0.1, "new": 0.0}'),
(19, NULL, 'happy', '{"happy": 0.6, "excited": 0.25, "depressed": 0.05, "angry": 0.0, "anxious": 0.0, "bored": 0.0, "sad": 0.1, "new": 0.0}'),
(20, NULL, 'happy', '{"happy": 0.55, "excited": 0.1, "depressed": 0.1, "angry": 0.0, "anxious": 0.05, "bored": 0.05, "sad": 0.15, "new": 0.0}');

-- ============================================
-- 인덱스 생성 (성능 최적화)
-- ============================================
CREATE INDEX IF NOT EXISTS idx_mood_logs_user_id ON mood_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_mood_logs_created_at ON mood_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_movie_sentiments_movie_id ON movie_sentiments(movie_id);

-- 데이터 확인 쿼리
-- SELECT COUNT(*) as user_count FROM users;
-- SELECT COUNT(*) as movie_count FROM movies;
-- SELECT COUNT(*) as genre_count FROM genres;
-- SELECT COUNT(*) as movie_genre_count FROM movie_genres;
-- SELECT COUNT(*) as review_count FROM reviews;
-- SELECT COUNT(*) as mood_log_count FROM mood_logs;
-- SELECT COUNT(*) as sentiment_count FROM movie_sentiments;

