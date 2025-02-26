import sqlite3

# SQLite 데이터베이스 연결 (없으면 생성됨)
conn = sqlite3.connect("cosme.db")
cursor = conn.cursor()

# # 기존 테이블 삭제 (있으면 삭제)
# cursor.execute("DROP TABLE IF EXISTS product")
# cursor.execute("DROP TABLE IF EXISTS category")
# cursor.execute("DROP TABLE IF EXISTS brand")
# cursor.execute("DROP TABLE IF EXISTS rank")
# cursor.execute("DROP TABLE IF EXISTS review")

# products 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_id TEXT PRIMARY KEY,         -- 기본 키 (PK)
    brand_id TEXT,                       -- 브랜드 ID (외래 키)
    category_id TEXT,                    -- 카테고리 ID (외래 키)
    rating REAL,                            -- 평점 (소수점 가능)
    review_cnt INTEGER,                     -- 리뷰 개수
    price TEXT,                             -- 가격
    update_date DATE,                       -- 업데이트 날짜
    url TEXT,                               -- 제품 URL
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
""")

# categories 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS category (
    category_id TEXT PRIMARY KEY,  -- 기본 키 (PK)
    category_name TEXT,               -- 카테고리 이름 (일본어)
    category_name_kr TEXT             -- 카테고리 이름 (한국어)
);
""")

# brands 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS brand (
    brand_id TEXT PRIMARY KEY,      -- 기본 키 (PK)
    brand_name TEXT ,            -- 브랜드 이름 (일본어, 고유)
    brand_name_kr TEXT ,                -- 브랜드 이름 (한국어)
    brand_url TEXT               -- 브랜드 URL (고유)
);
""")

# rank 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS rank (
    rank_id INTEGER PRIMARY KEY,      -- 기본 키 (PK)
    product_id TEXT,                   -- 제품 아이디 (FK)
    ranking INTEGER,                -- 순위 (한국어)
    date DATE                     -- 업데이트 날짜
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS review (
    review_id TEXT PRIMARY KEY,      -- 기본 키 (PK)
    product_id TEXT,                   -- 제품 아이디 (FK)
    reviewer_name TEXT,
    age TEXT,
    skin_type TEXT,
    rating INTEGER,                -- 순위 (한국어)
    purchase_info TEXT,
    review_date DATE                     -- 업데이트 날짜
);
""")

# 변경 사항 저장 & 연결 종료
conn.commit()
conn.close()
