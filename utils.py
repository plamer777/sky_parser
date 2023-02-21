import json
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def clean_digits(data: str) -> int:
    result = re.sub(r'\D*', '', data)
    return int(str(result))


def load_from_json(filename: str) -> dict:
    try:
        with open(filename, encoding='utf-8') as fin:
            return json.load(fin)

    except Exception as e:
        print(f"There was an error during loading from JSON: {e}")
        return {}


def init_sync_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=640x480")
    options.add_argument("'--blink-settings=imagesEnabled=false'")

    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()

    return driver


def update_parsed_data(parse_data: dict):
    price = parse_data.get('price')
    period = parse_data.get('period')
    price = clean_digits(price)
    period = clean_digits(period)

    parse_data['price'] = price
    parse_data['period'] = period
    parse_data['total'] = price * period

    return parse_data



