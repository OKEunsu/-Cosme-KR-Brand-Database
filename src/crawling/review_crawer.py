import requests
from bs4 import BeautifulSoup
import json
import time
import random
import sqlite3
import logging
import re
import pandas as pd

# 로그 파일 및 설정
logging.basicConfig(
    filename='review_crawler.log',  # 로그를 저장할 파일 경로
    level=logging.INFO,  # 로그 레벨 설정: INFO 이상 기록
    format='%(asctime)s - %(levelname)s - %(message)s'  # 로그 형식
)

with open("weburl.json", "r", encoding="utf-8") as f:
    cosme_url = json.load(f)

# 크롬 브라우저의 User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
# product_id 가져오기
def get_product_id():
    conn = sqlite3.connect(r'C:\Users\WD\PycharmProjects\Cosme-KR-Brand-Database\data\cosme.db')
    cursor = conn.cursor()

    cursor.execute("select product_id from product")
    product_ids = cursor.fetchall()
    # 결과를 일반 리스트로 변환 (튜플에서 첫 번째 요소만 가져오기)
    product_ids_list = [product_id[0] for product_id in product_ids]

    logging.info(f"Sucessfull get product id")
    # 연결 종료
    conn.close()
    return product_ids_list

# product_id, 마지막 페이지 숫자
def extract_page_num(product_id):
    base_url = cosme_url['review'] + f"/{product_id}/review/?page=1"

    # HTTP 요청 보내기 (User-Agent 포함)
    response = requests.get(base_url, headers=headers)
    time.sleep(random.uniform(3,5))

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    page_numbers = [
        int(li.text) for li in soup.find("ul", class_="number").find_all("li") if li.text.isdigit()
    ]
    logging.info(f"Sucessfull Find Max page number")
    return max(page_numbers)

def extract_data_from_page(product_id, num):
    base_url = cosme_url['review'] + f"/{product_id}/review/?page={num}"

    # HTTP 요청 보내기 (User-Agent 포함)
    response = requests.get(base_url, headers=headers)
    time.sleep(random.uniform(3,5))

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def extract_reviewer(soup):
    name_list = []
    for name in soup.find_all("span", class_="reviewer-title"):
        name_list.append(name.text)
    return name_list

def extract_review_list(soup):
    # 리뷰 리스트 가져오기
    review_list = soup.find("div", id="product-review-list").find_all("ul")

    # 데이터 저장용 리스트
    age_list = []
    skin_type_list = []
    review_count_list = []
    links = [tag.find("a").get('href') for tag in soup.find_all("span", class_="read-more") if tag.find("a")]
    review_id = [re.search(r"\d+", link).group() for link in links]

    for ul in review_list:
        li_tags = ul.find_all("li")

        if len(li_tags) >= 3:  # 연령대, 피부 타입, 리뷰 개수 정보가 있는 경우만 처리
            age = li_tags[0].text.strip() if len(li_tags) > 0 else None
            skin_type = li_tags[1].text.strip() if len(li_tags) > 1 else None
            review_count = li_tags[2].find("span").text.strip() if li_tags[2].find("span") else "0"

            age_list.append(age)
            skin_type_list.append(skin_type)
            review_count_list.append(review_count)
        else:
            # Append None or default values if necessary
            age_list.append(None)
            skin_type_list.append(None)
            review_count_list.append("0")

    # Ensure review_id list is always the same length as other lists
    missing_ids = len(age_list) - len(review_id)
    review_id.extend([None] * missing_ids)  # Append None if review_id is shorter

    return age_list, skin_type_list, review_count_list, review_id


def extract_review_info(soup):
    rating_list = []
    purchase_info_list = []
    review_date_list = []

    # 리뷰들에서 별점과 날짜 추출
    reviews = soup.find_all("div", class_="rating clearfix")

    # 각 리뷰에서 화장품명, 별점, 구매 정보, 날짜를 출력
    for review in reviews:
        # 별점 추출
        rating_tag = review.find("p", class_="reviewer-rating")
        if rating_tag:
            rating_text = rating_tag.text.strip()  # 예: '3購入品'
            rating = re.sub(r'\D', '', rating_text)  # 숫자만 추출 (예: '3')
            purchase_info = re.sub(r'\d', '', rating_text).strip()  # 숫자를 제외한 나머지 (예: '購入品')
            rating_list.append(rating)
            purchase_info_list.append(purchase_info)
        else:
            rating = None
            purchase_info = None

        # 날짜 추출
        date_tag = review.find(["p"], class_=["mobile-date", "date"])
        if date_tag:
            review_date = date_tag.text.strip()  # 리뷰 작성 날짜 (예: '2025/2/26 19:39:13')
            review_date_list.append(review_date)
        else:
            review_date = None
    return rating_list, purchase_info_list, review_date_list

if __name__  == '__main__':
    review_id_list = []
    product_id_list = []
    reviewer_name_list = []
    age_list = []
    skin_type_list = []
    rating_list = []
    purchase_info_list = []
    review_date_list = []

    product_ids_list = get_product_id()
    for product_id in product_ids_list:
        max_page = extract_page_num(product_id)
        for num in range(1, max_page+1):
            # product_id
            product_id_list.append(product_id)
            soup = extract_data_from_page(product_id, num)
            # 닉네임
            name = extract_reviewer(soup)
            reviewer_name_list.extend(name)

            # 리뷰 아이디, 나이, 스킨타입
            age, skin_type, _ , review_id = extract_review_list(soup)
            age_list.extend(age)
            skin_type_list.extend(skin_type)
            review_id_list.extend(review_id)

            rating, purchase_info, review_date = extract_review_info(soup)
            rating_list.extend(rating)
            purchase_info_list.extend(purchase_info)
            review_date_list.extend(review_date)

        print(f"Length of review_id_list: {len(review_id_list)}")
        print(f"Length of product_id_list: {len(product_id_list)}")
        print(f"Length of reviewer_name_list: {len(reviewer_name_list)}")
        print(f"Length of age_list: {len(age_list)}")
        print(f"Length of skin_type_list: {len(skin_type_list)}")
        print(f"Length of rating: {len(rating_list)}")
        print(f"Length of purchase_info: {len(purchase_info_list)}")
        print(f"Length of review_date: {len(review_date_list)}")

        df = pd.DataFrame({
            'review_id': review_id_list,
            'product_id' : product_id_list,
            "reviewer_name": reviewer_name_list,
            "age": age_list,
            "skin_type": skin_type_list,
            "rating": rating_list,
            "purchase_info": purchase_info_list,
            "review_date": review_date_list
        })

        # SQLite 데이터베이스 연결
        logging.info(f"Inserting data into database...")
        conn = sqlite3.connect(r'C:\Users\WD\PycharmProjects\Cosme-KR-Brand-Database\data\cosme.db')
        cursor = conn.cursor()

        for index, row in df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO review (review_id, product_id, reviewer_name, age, skintype, rating, purchase_info, review_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['review_id'], row['product_id'], row['reviewer_name'], row['age'], row['skintype'], row['rating'], row['purchase_info'], row['review_date']))
        logging.info("Data successfully inserted into the review_db.")

        conn.commit()  # 변경사항 저장
        conn.close()  # 연결 종료
        logging.info("Database connection closed.")
