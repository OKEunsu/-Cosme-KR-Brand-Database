import re

def extract_id(url):
    """
    주어진 URL에서 ID를 추출하는 함수.
    'brands/{id}', 'products/{id}', 'categories/{id}', 'categories/item/{id}' 경로가 있는 URL을 처리.

    Parameters:
        url (str): URL

    Returns:
        str: ID 또는 None (ID가 없는 경우)
    """
    match = re.search(r'(?:brands|products|categories(?:/item)?)/(\d+)', url)
    if match:
        return match.group(1)  # ID 반환
    return None  # ID가 없는 경우 None 반환

def extract_price_info(price_tags):
    price_list = []  # 변환된 가격 정보를 저장할 리스트

    for tag in price_tags:
        price_text = tag.text.replace("税込価格：", "").strip()  # "税込価格：" 제거 후 텍스트 추출
        price_items = price_text.split(" / ")  # 여러 개의 가격이 있으면 분리

        price_dict = {}  # 한 제품의 가격 정보를 저장할 딕셔너리

        for item in price_items:
            match = re.match(r"(.+?)・([\d,]+円)", item)  # "단위・가격" 패턴 추출
            if match:
                unit = match.group(1).strip()  # 단위 (예: "5.3g", "1枚", "4枚")
                price = match.group(2).strip()  # 가격 (예: "290円", "1,760円")
                price_dict[unit] = price  # 딕셔너리에 저장

        if price_dict:  # 비어 있지 않은 경우만 추가
            price_list.append(price_dict)
        else:
            price_list.append(price_text)  # 가격 정보가 없는 경우 그대로 추가

    return price_list

if __name__ == "__main__":
    # 테스트 데이터
    price_tags = [
        "税込価格：1枚・290円 / 4枚・1,090円",
        "税込価格：9g・1,210円",
        "税込価格：27ml×1枚入・275円 / 27ml×10枚入・2,750円 / 27ml×3枚入・825円",
        "税込価格：5.3g・1,760円",
        "税込価格：1枚・290円 / 4枚・1,090円",
        "税込価格：20g・1,870円 / 20g・2,365円 / 20g・2,750円",
        "税込価格：1,980円",  # 단위 없는 경우
        "税込価格：220ml・2,750円",
        "税込価格：11ml・880円",
        "税込価格：50ml・3,300円"
    ]
    # 함수 실행
    result = extract_price_info(price_tags)

    # 결과 출력
    print(result)
