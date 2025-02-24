import re

def extract_price(price_text):
    """
    주어진 가격 박스에서 가격 가져오기

    Parameters:
        price_text (str): 가격 박스

    Returns:
        int: price
    """

    if not price_text:
        return 0  # 가격이 비어 있으면 0 반환

    try:
        # 정규표현식을 사용하여 숫자만 추출
        price_numbers = re.findall(r'(\d+,?\d*)', price_text)
        if price_numbers:
            # 쉼표 제거 후 정수형으로 반환
            final_price = price_numbers[-1].replace(',', '')
            return int(final_price)  # 정수형으로 반환
        return 0  # 숫자가 없는 경우 기본값
    except Exception as e:
        print(f"Error: {e}")
        return 0  # 예외가 발생할 경우 기본값


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



if __name__ == "__main__":
    price = '税込価格：1枚・290円 / 4枚・1,090円'
    return_price = extract_price(price)
    category =  'https://www.cosme.net/categories/item/1007/'
    return_category = extract_id(category)

    print(price)
    print(return_price)

    print(category)
    print(return_category)
