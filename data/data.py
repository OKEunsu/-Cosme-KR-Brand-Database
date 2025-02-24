import sqlite3

# SQLite 데이터베이스 연결 (없으면 생성됨)
conn = sqlite3.connect("product.db")
cursor = conn.cursor()

# products 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,         -- 기본 키 (PK)
    brand_id INTEGER,                       -- 브랜드 ID (외래 키)
    category_id INTEGER,                     -- 카테고리 ID (외래 키)
    rating REAL,                            -- 평점 (소수점 가능)
    review_cnt INTEGER,                     -- 리뷰 개수
    price INTEGER,                          -- 가격
    release_info DATE,                      -- 출시일 (YYYY-MM-DD 형식)
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

# 변경 사항 저장 & 연결 종료
conn.commit()
conn.close()

# SQLite 데이터베이스 연결
conn = sqlite3.connect("category.db")
cursor = conn.cursor()

# categories 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,  -- 기본 키 (PK)
    category_name TEXT,               -- 카테고리 이름 (일본어)
    category_name_kr TEXT             -- 카테고리 이름 (한국어)
);
""")

# 변경 사항 저장 & 연결 종료
conn.commit()
conn.close()

# SQLite 데이터베이스 연결
conn = sqlite3.connect("brand.db")
cursor = conn.cursor()

# categories 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    brand_id INTEGER PRIMARY KEY,  -- 기본 키 (PK)
    brand_name TEXT,               -- 브랜드 이름 (일본어)
    brand_name_kr TEXT             -- 브랜드 이름 (한국어)
    brand_url TEXT
);
""")

# 변경 사항 저장 & 연결 종료
conn.commit()
conn.close()



