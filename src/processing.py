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

def parse_price(price_str):
    price_dict = {}
    price_str = price_str.replace("税込価格：", "").replace("\xa0", " ").strip()  # "税込価格：" & 비브레이킹 스페이스 제거

    # `/`로 여러 가격 옵션을 나누기
    price_options = price_str.split(" / ")

    for option in price_options:
        # "단위・가격円" 패턴 찾기
        match = re.match(r'(.+?)・([\d,]+)円', option)
        if match:
            size, price = match.groups()
            price_dict[size] = int(price.replace(",", ""))  # 숫자 변환

    # 단순 가격 패턴 처리 (예: "1,980円" → "単品")
    if not price_dict:
        simple_price_match = re.search(r'([\d,]+)円$', price_str)
        if simple_price_match:
            price_dict["単品"] = int(simple_price_match.group(1).replace(",", ""))

    return price_dict
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
