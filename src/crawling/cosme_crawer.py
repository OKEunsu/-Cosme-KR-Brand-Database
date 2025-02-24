from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
from src.processing import extract_price, extract_id

# JSON 파일 읽기
with open("weburl.json", "r", encoding="utf-8") as f:
    cosme_url = json.load(f)  # 파일을 Python 딕셔너리로 변환

print(cosme_url["ranking"])  # 'ranking' 키 값 출력

now = datetime.now()  # 현재 날짜 및 시간
date = now.date()     # 현재 날짜 (년-월-일)

# 크롬 브라우저의 User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# HTTP 요청 보내기 (User-Agent 포함)
response = requests.get(cosme_url["ranking"], headers=headers)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

if __name__ == "__main__":
    print(cosme_url["ranking"] + f"?page{date}")