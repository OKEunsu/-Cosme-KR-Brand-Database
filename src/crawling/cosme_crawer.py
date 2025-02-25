import random
import time
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pandas as pd
from sqlalchemy import create_engine
from src.processing import parse_price, extract_id
import sqlite3
import logging

# 로그 파일 및 설정
logging.basicConfig(
    filename='cosme_crawler.log',  # 로그를 저장할 파일 경로
    level=logging.INFO,  # 로그 레벨 설정: INFO 이상 기록
    format='%(asctime)s - %(levelname)s - %(message)s'  # 로그 형식
)

# 웹페이지에서 데이터를 추출하는 함수
def extract_data_from_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to retrieve {url} with status code {response.status_code}")
            return None
        logging.info(f"Successfully retrieved {url}")
        time.sleep(random.uniform(3, 5))  # 시간 간격 두기
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        logging.error(f"Request error for {url}: {str(e)}")
        return None
# 브랜드 정보 추출
def extract_brands(soup):
    brand_names, brand_links = [], []
    brands = soup.find_all("span", class_="brand")
    if not brands:
        logging.warning("No brands found on the page")
    for span in brands:
        a_tag = span.find("a")
        if a_tag:
            brand_names.append(a_tag.text)
            brand_links.append(a_tag.get("href"))
    logging.info(f"Found {len(brand_names)} brands")
    return brand_names, brand_links
def extract_products(soup):
    product_names, product_links = [], []
    items = soup.find_all("h4", class_="item")
    if not items:
        logging.warning("No products found on the page")
    for span in items:
        a_tag = span.find("a")
        if a_tag:
            product_names.append(a_tag.text)
            product_links.append(a_tag.get("href"))
    logging.info(f"Found {len(product_names)} products")
    return product_names, product_links
# 카테고리 정보 추출
def extract_categories(soup):
    category_ids = []
    categorys = soup.find_all('span', class_='category')
    for category in categorys:
        links = category.find_all('a')
        category_ids.append([extract_id(link['href']) for link in links])
    return category_ids
# 리뷰 수 추출
def extract_reviews(soup):
    review_list = []
    review_tags = soup.find_all("a", class_="count")
    for review_tag in review_tags:
        review_count = review_tag.get_text().strip()
        review_list.append(review_count)
    return review_list
# 평점 정보 추출
def extract_ratings(soup):
    rating_list = []
    rating_point_tags = soup.find_all("div", class_="rating-point clearfix")
    for rating_point_tag in rating_point_tags:
        rating_tag = rating_point_tag.find("p", class_=["rating", "reviewer-average", "arg-5", "arg-6"])
        if rating_tag:
            rating = rating_tag.get_text().strip()
            rating_list.append(float(rating))
    return rating_list
# 발매일 추출
def extract_onsale_dates(soup):
    onsale_date = []
    release_date_tags = soup.find_all("p", class_="onsale")
    for release_date in release_date_tags:
        if release_date:
            onsale_date.append(release_date.text[6:])
    return onsale_date
# 가격 추출
def extract_prices(soup):
    price_list = []
    price_tags = soup.find_all("p", class_="price")  # 여러 개의 태그 반환
    for tag in price_tags:
        price_list.append(tag.text)  # 텍스트를 가져오고 공백 제거
    return price_list
# 메인 크롤링
def crawling(num):
    logging.info(f"Starting crawling page {num}")
    soup = extract_data_from_page(cosme_url['ranking'] + f'?page={num}', headers)
    brand_names, brand_links = extract_brands(soup)
    brand_id = [extract_id(x) for x in brand_links]
    product_names, product_links = extract_products(soup)
    product_id = [extract_id(x) for x in product_links]
    category_id = extract_categories(soup)
    review_list = extract_reviews(soup)
    review_list_int = [int(re.search(r'\d+', review).group()) for review in review_list]
    rating_list = extract_ratings(soup)
    onsale_date = extract_onsale_dates(soup)
    price_list = extract_prices(soup)
    price_list_dict = [parse_price(x) for x in price_list]

    brand_id_list.extend(brand_id)
    brand_names_list.extend(brand_names)
    brand_links_list.extend(brand_links)
    product_id_list.extend(product_id)
    product_names_list.extend(product_names)
    product_links_list.extend(product_links)
    category_id_list.extend(category_id)
    review_list_int_list.extend(review_list_int)
    rating_list_list.extend(rating_list)
    onsale_date_list.extend(onsale_date)
    price_list_dict_list.extend(price_list_dict)
    logging.info(f"Finished crawling page {num}")

# JSON 파일 읽기
with open("weburl.json", "r", encoding="utf-8") as f:
    cosme_url = json.load(f)  # 파일을 Python 딕셔너리로 변환

# 크롬 브라우저의 User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 현재 날짜 및 시간
now = datetime.now()  # 현재 날짜 및 시간
date = now.date()     # 현재 날짜 (년-월-일)

if __name__ == '__main__':


    brand_id_list = []
    brand_names_list = []
    brand_links_list = []
    product_id_list = []
    product_names_list = []
    product_links_list = []
    category_id_list = []
    review_list_int_list = []
    rating_list_list = []
    onsale_date_list = []
    price_list_dict_list = []

    for page in range(1, 6):
        crawling(page)

    rank_list = [x for x in range(1, len(product_id_list)+1)]

    brand_db = pd.DataFrame({
        'brand_id' : brand_id_list,
        'brand_name' : brand_names_list,
        'brand_url' : brand_links_list
    })

    rank_db = pd.DataFrame({
        'product_id' : product_id_list,
        'ranking' : rank_list,
        'date': [date] * len(product_id_list)
    })

    product_db = pd.DataFrame({
        'product_id' : product_id_list,
        'brand_id' : brand_id_list,
        'category_id' : category_id_list,
        'rating' : rating_list_list,
        'review_cnt' : review_list_int_list,
        'price' : price_list_dict_list,
        'update_date' : [date] * len(product_id_list),
        'url' : product_links_list
    })
    # category_id와 price를 모두 문자열로 변환
    product_db['category_id'] = product_db['category_id'].apply(str)
    product_db['price'] = product_db['price'].apply(str)

    # SQLite 데이터베이스 연결
    logging.info(f"Inserting data into database...")
    conn = sqlite3.connect(r'C:\Users\WD\PycharmProjects\Cosme-KR-Brand-Database\data\cosme.db')
    cursor = conn.cursor()

    # 각 데이터프레임을 테이블에 추가 (append로 추가)
    rank_db.to_sql('rank', conn, if_exists='append', index=False)
    logging.info("Data successfully inserted into the rank_db.")

    for index, row in brand_db.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO brand (brand_id, brand_name, brand_url)
            VALUES (?, ?, ?)
        ''', (row['brand_id'], row['brand_name'], row['brand_url']))
    logging.info("Data successfully inserted into the brand_db.")

    for index, row in product_db.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO product
            (product_id, brand_id, category_id, rating, review_cnt, price, update_date, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['product_id'], row['brand_id'], row['category_id'], row['rating'], row['review_cnt'], row['price'],
              row['update_date'], row['url']))
    logging.info("Data successfully inserted into the product_db.")

    conn.commit()  # 변경사항 저장
    conn.close()  # 연결 종료
    logging.info("Database connection closed.")