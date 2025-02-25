import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random
from src.processing import extract_id
import pandas as pd
from sqlalchemy import create_engine

# 카테고리 아이디, 이름 크롤링
# # 크롬 브라우저의 User-Agent 설정
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
# }
#
# url = "https://www.cosme.net/category/#theme-items"
# # HTTP 요청 보내기 (User-Agent 포함)
# response = requests.get(url, headers=headers)
#
# time.sleep(random.uniform(3,5))
#
# # BeautifulSoup으로 HTML 파싱
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # <div id="theme-items"> 안의 세부 항목 찾기
# theme_items_div = soup.find("div", id="theme-items")
# category_links = []
# category_names = []
#
# if theme_items_div:
#     theme_lists = theme_items_div.find_all("ul", class_="theme-product-list")
#     for ul in theme_lists:
#         for li in ul.find_all("li"):
#             a_tag = li.find("a")
#             if a_tag:
#                 category_names.append(a_tag.text.strip())  # 카테고리명
#                 category_links.append(a_tag["href"])  # 링크 URL
#
# category_id = [extract_id(code) for code in category_links]
#
# df = pd.DataFrame({
#     "category_id" : category_id,
#     "category_name" : category_names
# })
#
# df = df.drop_duplicates()
# df.to_excel("category.xlsx", index=False)

# 엑셀에서 transelate([셀], 'ja', 'ko')을 작업 후 불러오기
df = pd.read_excel("category.xlsx")
print(df.head())

# SQLite DB 연결 (파일로 저장되는 DB)
engine = create_engine('sqlite:///cosme.db')

# pandas DataFrame을 DB에 업로드
df.to_sql('category', con=engine, if_exists='replace', index=False)
