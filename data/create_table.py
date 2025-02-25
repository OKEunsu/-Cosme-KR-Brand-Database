import sqlite3

# SQLite 데이터베이스 연결 (없으면 생성됨)
conn = sqlite3.connect("cosme.db")
cursor = conn.cursor()

# 기존 테이블 삭제 (있으면 삭제)
cursor.execute("DROP TABLE IF EXISTS product")
cursor.execute("DROP TABLE IF EXISTS category")
cursor.execute("DROP TABLE IF EXISTS brand")

# products 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_id INTEGER PRIMARY KEY,         -- 기본 키 (PK)
    brand_id INTEGER,                       -- 브랜드 ID (외래 키)
    category_id INTEGER,                    -- 카테고리 ID (외래 키)
    rating REAL,                            -- 평점 (소수점 가능)
    review_cnt INTEGER,                     -- 리뷰 개수
    price TEXT,                             -- 가격
    release_info TEXT,                      -- 출시일 (YYYY-MM-DD 형식)
    update_date DATE,                       -- 업데이트 날짜
    url TEXT,                               -- 제품 URL
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
""")

# categories 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS category (
    category_id INTEGER PRIMARY KEY,  -- 기본 키 (PK)
    category_name TEXT,               -- 카테고리 이름 (일본어)
    category_name_kr TEXT             -- 카테고리 이름 (한국어)
);
""")

# brands 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS brand (
    brand_id INTEGER PRIMARY KEY,      -- 기본 키 (PK)
    brand_name TEXT,                   -- 브랜드 이름 (일본어)
    brand_name_kr TEXT,                -- 브랜드 이름 (한국어)
    brand_url TEXT                     -- 브랜드 URL
);
""")

# 변경 사항 저장 & 연결 종료
conn.commit()
conn.close()
