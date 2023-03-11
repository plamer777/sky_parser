"""This file contains different utility functions to load and save data,
refactor dictionaries, etc."""
import json
import re
from concurrent.futures import Future
from datetime import datetime
from typing import Any, Union, Iterator
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from constants import PRICE_TYPES, LEVELS, SERVICE_TAGS, \
    INITIAL_PARSE_DATA, PRICE_LEVELS, REFACTOR_TAGS, PRICE_TAGS
from create_loggers import logger
from parse_classes.schools import SchoolParseTask, \
    ProfessionParseRequest


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
    except (ValueError, TypeError):
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
    for row in data:
        for price_tag in PRICE_TAGS:
            new_row = row.copy()
            tag = new_row.get(price_tag, None)
            price = new_row.pop(PRICE_LEVELS[tag], None)
            new_row = remove_excessive_data(new_row)

            if tag:
                new_row['course_level'] = LEVELS[PRICE_LEVELS[tag]]
                new_row['price'] = price
                new_row = update_parsed_data(new_row)
                result.append(new_row)

    return result


def init_sync_driver() -> WebDriver | None:
    """This function initializes the sync selenium driver to parse sites with
    JS or having another problems for standard asynchronous parsing
    :return: a configured WebDriver instance
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=640x480")
        options.add_argument("'--blink-settings=imagesEnabled=false'")

        driver = webdriver.Chrome(options=options)
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
        parse_data['total'] = round(price * period) if price and period else ''
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
    [data.pop(tag, None) for tag in SERVICE_TAGS]

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
            old_price, new_price = prof_old.get('price'), prof_new.get('price')
            old_period, new_period = prof_old.get('period'), prof_new.get(
                'period')

            prof_new['price_change'] = new_price - old_price \
                if type(new_price) is int and type(old_price) is int else 0

            prof_new['period_change'] = new_period - old_period \
                if type(new_period) is int and type(old_period) is int else 0

            professions.append(prof_new)

        new_data[key] = professions

    return new_data


def sort_parsed_unparsed(
        data: Union[Iterator[Future], list[dict]]) -> tuple[list, list]:
    """This function sorts provided data into parsed and unparsed
    :param data: a list of dictionaries or Iterator containing Futures
    :return: a tuple of lists of parsed and unparsed data
    """
    unparsed = []
    parsed = []
    for row in data:
        if type(row) is Future:
            row = row.result()
        if not row.get('price'):
            print(f'{row.get("url")} failed, one more attempt')
            unparsed.append(row)
        else:
            print(f'Task {row.get("url")} finished')
            parsed.append(row)

    return parsed, unparsed


def refactor_parse_tags(data: dict[str, list[dict]]) -> list[dict]:
    """This function serves to refactor initial dictionary with parse data to
    upload in Google Sheets
    :param data: a dictionary with parse data
    :return: a list of refactored dictionaries
    """
    for key in data:
        for row in data[key]:
            for price_tag in REFACTOR_TAGS:

                tag = row.get(price_tag, None)

                if tag:
                    created_row = {'school': key,
                                   'profession': row['profession'],
                                   'tags_type': price_tag,
                                   'price_tags': tag}

                    yield created_row


def convert_table_data_to_json(data: list[list]) -> dict[str, list[dict]]:
    """This function serves to convert a list of lists loaded from Google
    Sheets into dictionary
    :param data: a list of lists
    :return: a dictionary containing converted data
    """
    result = {}
    parse_tasks = []
    single_task = SchoolParseTask()
    previous_school = ''
    prof_list = []
    current_profession = INITIAL_PARSE_DATA.copy()
    for row in data:
        school, prof, tag_type = row[:3]
        tags = row[3:]

        if current_profession != INITIAL_PARSE_DATA \
                and prof not in current_profession.values():

            prof_list.append(current_profession)
            single_task.parse_requests.append(
                ProfessionParseRequest(**current_profession))

            current_profession = INITIAL_PARSE_DATA.copy()

        if result and school not in result:
            result[previous_school].extend(prof_list)
            single_task.school_name = previous_school  # оставить только то,
            # что создает отдельный словарь с данными для парсинга
            parse_tasks.append(single_task)
            single_task = SchoolParseTask()
            current_profession = INITIAL_PARSE_DATA.copy()
            prof_list = []

        result.setdefault(school, [])
        current_profession['profession'] = prof

        if tag_type != 'url':
            if tag_type != 'additional_price_tags':
                current_profession[PRICE_LEVELS[tag_type]] = ''
            current_profession.setdefault(tag_type, []).extend(tags)
        else:
            current_profession[tag_type] = tags[0]

        previous_school = school

    single_task.parse_requests.append(
        ProfessionParseRequest(**current_profession))
    parse_tasks.append(single_task)
    prof_list.append(current_profession)
    result[school].extend(prof_list)

    return result


def convert_json_to_table_data(data: dict[str, list]) -> list[list]:
    """This function converts dictionary with parse data into a list of lists
    :param data: a dictionary with parse data
    :return: a list of lists
    """
    rows = []
    for row in refactor_parse_tags(data):
        new_row = [row['school'], row['profession'], row['tags_type'],
                   ]
        if row['tags_type'] == 'url':
            new_row.append(row['price_tags'])
        else:
            new_row.extend(row['price_tags'])

        rows.append(new_row)

    return rows

# schools = load_from_json('data/schools_new.json')
#
# result = []
# for school in schools:
#     new_school = School(
#         name=school,
#         professions=[Profession(**item) for item in schools[school]])
#
#     result.append(new_school)
#
# print(result)

