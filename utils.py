"""This file contains different utility functions to load and save data,
refactor dictionaries, etc."""
import json
import re
from datetime import datetime
from typing import Any, Union
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from constants import DRIVER_PATH
from create_loggers import logger
# ------------------------------------------------------------------------


def clean_digits(data: Union[int, str]) -> int:
    """This function serves to remove any characters from provided data except
    digits
    :param data: a string containing digits or integer otherwise
    :return: an integer
    """
    try:
        result = re.sub(r'\D*', '', data)
        result = int(str(result))
        return result
    except (ValueError, TypeError) as e:
        logger.error(f"There was an error in cleaning_digits function: {e}")
        return data


def load_from_json(filename: str) -> dict:
    """This function reads data from a json file
    :param filename: path to json file
    :return: dictionary or list of dictionaries loaded from json file
    """
    try:
        with open(filename, encoding='utf-8') as fin:
            return json.load(fin)

    except Exception as e:
        logger.error(f"There was an error during loading from JSON: {e}")
        return {}


def refactor_data(data: list[dict]) -> list[dict]:
    """refactor_data function serves to change provided data structure. It
    can make up to 3 dictionaries from each provided if there are special
    fields in the dictionaries
    :param data: a list of dictionaries
    :return: a list of refactored dictionaries
    """
    result = []
    for raw in data:
        raw = remove_excessive_data(raw)
        middle_price = raw.pop('middle_price', None)
        pro_price = raw.pop('pro_price', None)

        raw['course_level'] = 'basic'
        raw = update_parsed_data(raw)
        result.append(raw)

        if middle_price:
            raw = raw.copy()
            raw['course_level'] = 'middle'
            raw['price'] = middle_price
            raw = update_parsed_data(raw)
            result.append(raw)
        if pro_price:
            raw = raw.copy()
            raw['course_level'] = 'pro'
            raw['price'] = pro_price
            raw = update_parsed_data(raw)
            result.append(raw)

    return result


def init_sync_driver() -> WebDriver | None:
    """This function initializes the sync selenium driver to parse sites with
    JS or having another problems for standard asynchronous parsing
    :return: a configured WebDriver instance
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=640x480")
        options.add_argument("'--blink-settings=imagesEnabled=false'")

        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        return driver
    except Exception as e:
        logger.error(
            f'There was an error in the init_sync_driver function: {e}')
        return None


def update_parsed_data(parse_data: dict[str, Any]) -> dict[str, Any]:
    """This function updates provided parse_data dictionary
    :param parse_data: a dictionary containing parsed data to update
    :return: updated dictionary with initial data
    """
    price = parse_data.get('price')
    period = parse_data.get('period')
    price = clean_digits(price)
    period = clean_digits(period)

    try:
        parse_data['price'] = price
        parse_data['period'] = period
        parse_data['total'] = round(price * period)
        parse_data['price_change'] = 0
        parse_data['period_change'] = 0
        parse_data['updated_at'] = str(datetime.now()).split('.')[0]
    except Exception as e:
        logger.error(
            f'There was an error in the update_parsed_data function: {e}')

    return parse_data


def save_data_to_json(data: dict[str, list], filename: str) -> None:
    """This function saves data to json file
    :param data: a dictionary containing data to save
    :param filename: the file path to save
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    except Exception as e:
        logger.error(f"There was an error during saving to JSON: {e}")


def remove_excessive_data(data: dict[str, Any]) -> dict[str, Any]:
    """This functions serves to remove service info before sending to google
    tables
    :param data: parsed data to remove keys from
    :return: dictionary without excessive info
    """
    data.pop('price_tags', None)
    data.pop('period_tags', None)
    data.pop('total_tags', None)
    data.pop('additional_price_tags', None)
    data.pop('middle_price_tags', None)
    data.pop('pro_price_tags', None)

    return data


def compare_data(old_data: dict[str, list], new_data: dict[str, list]):
    """This function serves to compare parsed data with loaded from json file
    :param old_data: dictionary with previous parse data
    :param new_data: dictionary with new parse data
    :return: an updated dictionary
    """
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
