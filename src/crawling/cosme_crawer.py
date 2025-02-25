import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
from src.processing import extract_price_info, extract_id
import time
import re
import pandas as pd

# JSON 파일 읽기
with open("weburl.json", "r", encoding="utf-8") as f:
    cosme_url = json.load(f)  # 파일을 Python 딕셔너리로 변환

# 현재 날짜 및 시간
now = datetime.now()  # 현재 날짜 및 시간
date = now.date()     # 현재 날짜 (년-월-일)

# 크롬 브라우저의 User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

brand_names = []
brand_links = []
# brand_id -> brand_links 변환

product_names = []
product_links = []
# product_id -> product_links 변환

category_links = []
category_names = []
category_ids = []

price_list = []
rating_list = []
review_list = []
onsale_date = []


for num in range(1, 6):
    url = cosme_url["ranking"] + f"?page={num}"

    # HTTP 요청 보내기 (User-Agent 포함)
    response = requests.get(url, headers=headers)

    time.sleep(random.uniform(3,5))

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 브랜드
    brands = soup.find_all("span", class_="brand")

    for span in brands:
        a_tag = span.find("a")  # <span> 안의 <a> 태그 추출
        if a_tag:
            brand_names.append(a_tag.text)
            brand_links.append(a_tag.get("href"))

    # 제품
    items = soup.find_all("h4", class_="item")
    for span in items:
        a_tag = span.find("a")
        if a_tag:
            product_names.append(a_tag.text)
            product_links.append(a_tag.get("href"))

    # 카테고리 정보 추출
    categorys = soup.find_all('span', class_='category')
    for category in categorys:
        links = category.find_all('a')
        category_names_in_product = []  # 한 제품에 대해 여러 카테고리를 담을 리스트
        category_links_in_product = []
        for link in links:
            category_names_in_product.append(link.text)
            category_links_in_product.append(link['href'])

        # 한 제품에 대한 카테고리들을 리스트에 추가
        category_names.append(category_names_in_product)
        category_links.append(category_links_in_product)
        category_ids.append([extract_id(link['href']) for link in links])

    # 평점
    rating_point_tags = soup.find_all("div", class_="rating-point clearfix")
    for rating_point_tag in rating_point_tags:
        rating_tag = rating_point_tag.find("p", class_=["rating", "reviewer-average", "arg-5", "arg-6"])
        if rating_tag:
            rating = rating_tag.get_text().strip()  # 평점 텍스트 추출
            rating_list.append(float(rating))

    # 리뷰 수
    review_tags = soup.find_all("a", class_="count")
    for review_tag in review_tags:
        review_count = review_tag.get_text().strip()  # 리뷰 수 텍스트
        review_list.append(review_count)

    # 발매일
    release_date_tags = soup.find_all("p", class_="onsale")
    for release_date in release_date_tags:
        if release_date:
            onsale_date.append(release_date.text[6:])

    # 가격
    price_tags = soup.find_all("p", class_="price")
    price_list.extend(price_tags)


review_list_int = [int(re.search(r'\d+', review).group()) for review in review_list]
brand_id = [extract_id(link) for link in brand_links]
product_id = [extract_id(link) for link in product_links]
price_list_dict = extract_price_info(price_list)

products_data = {
    "product_id": product_id,
    "brand_id": brand_id,
    "category_id": category_ids,
    "rating": rating_list,
    "review_cnt": review_list_int,
    "price": [str(price_dict) for price_dict in price_list_dict],
    "release_info": onsale_date,
    "url": product_links
}
categories_data = {
    "category_id": category_ids,
    "category_name": category_names
}
brands_data = {
    "brand_id": brand_id,
    "brand_name": brand_names,
    "brand_url": brand_links
}
# pandas 데이터프레임으로 변환
products_df = pd.DataFrame(products_data)
categories_df = pd.DataFrame(categories_data)
brands_df = pd.DataFrame(brands_data)

products_df.to_csv("product.csv", index=False, encoding = 'utf-8-sig')
categories_df.to_csv("categories.csv", index=False, encoding = 'utf-8-sig')
brands_df.to_csv("brands.csv", index=False, encoding = 'utf-8-sig')
