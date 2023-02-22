import json
import re
from datetime import datetime
from typing import Any
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from constants import DRIVER_PATH
# ------------------------------------------------------------------------


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


def init_sync_driver() -> WebDriver:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=640x480")
    options.add_argument("'--blink-settings=imagesEnabled=false'")

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    return driver


def update_parsed_data(parse_data: dict[str, Any]) -> dict[str, Any]:
    price = parse_data.get('price')
    period = parse_data.get('period')
    price = clean_digits(price)
    period = clean_digits(period)

    parse_data['price'] = price
    parse_data['period'] = period
    parse_data['total'] = price * period
    parse_data['price_change'] = 0
    parse_data['period_change'] = 0
    parse_data['url'] = parse_data.pop('url')
    parse_data['updated_at'] = str(datetime.now()).split('.')[0]

    return parse_data


def save_data_to_json(data: dict, filename: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    except Exception as e:
        print(f"There was an error during saving to JSON: {e}")


def remove_excessive_data(data: dict[str, list]) -> dict[str, list]:
    """This functions serves to remove service info before sending to google
    tables
    :param data: parsed data to remove keys from
    :return: dictionary without excessive info
    """
    for key in data:
        for value in data[key]:
            try:
                value.pop('price_tags')
                value.pop('period_tags')
                value.pop('total_tags')
            except KeyError:
                pass

    return data


def compare_data(old_data: dict[str, list], new_data: dict[str, list]):

    for key in old_data:
        old_data[key].sort(key=lambda x: x['profession'])
        new_data[key].sort(key=lambda x: x['profession'])

        professions = []
        for prof_old, prof_new in zip(old_data[key], new_data[key]):

            price_diff = prof_new['price'] - prof_old['price'] if prof_old[
                'price'] else 0
            period_diff = prof_new['period'] - prof_old['period'] if prof_old[
                'period'] else 0

            prof_new['price_change'] = price_diff
            prof_new['period_change'] = period_diff

            professions.append(prof_new)

        new_data[key] = professions

    return new_data
