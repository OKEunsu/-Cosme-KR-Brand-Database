import sqlite3
import pandas as pd
import json

# JSON 파일로부터 브랜드 한국어 이름 맵핑 불러오기
with open('brand_kr.json', 'r', encoding='utf-8') as f:
    brand_name_kr_mapping = json.load(f)

# SQLite 데이터베이스 연결
conn = sqlite3.connect("cosme.db", timeout=5)
cursor = conn.cursor()

# 'brand' 테이블에서 데이터 불러오기
cursor.execute("select * from brand")
df = pd.DataFrame(cursor.fetchall(), columns=['brand_id', 'brand_name', 'brand_name_kr', 'brand_url'])

# 'brand_name'을 기준으로 'brand_name_kr' 컬럼 채우기
df['brand_name_kr'] = df['brand_name'].map(brand_name_kr_mapping)

# 'brand' 테이블에 업데이트된 데이터를 반영
for index, row in df.iterrows():
    cursor.execute(''' 
        UPDATE brand
        SET brand_name_kr = ?
        WHERE brand_id = ?
    ''', (row['brand_name_kr'], row['brand_id']))

# 변경 사항 커밋하고 커서 닫기
conn.commit()
cursor.close()
conn.close()
