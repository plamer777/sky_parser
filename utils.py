"""This file contains different utility functions to load and save data,
refactor dictionaries, etc."""
import json
import os
import subprocess
import re
from datetime import datetime
from typing import Any, Union
from constants import (LEVELS, SERVICE_TAGS,
                       REFACTOR_TAGS, PRICE_TYPES, PERIODS)
from create_loggers import logger
from parse_classes.school_parse_task import SchoolParseTask, \
    ProfessionParseRequest, ProfessionParseResponse
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


def refactor_parse_responses(
        data: list[ProfessionParseResponse]) -> list[ProfessionParseResponse]:
    """The refactor_data function serves to change provided data structure. It
    can make up to 3 instances from each provided if there are special
    fields in the ProfessionParseResponse dictionaries
    :param data: a list of ProfessionParseResponse instances
    :return: a list of refactored instances
    """
    result = []
    for row in data:
        for price_type in PRICE_TYPES:

            price = getattr(row, price_type, '')
            if price is not None:
                new_row = ProfessionParseResponse.from_orm(row)
                try:
                    new_row.course_level = LEVELS[price_type]
                    new_row.price = price
                    period = getattr(new_row, PERIODS[price_type], None)
                    new_row.period = period if period else new_row.period
                    new_row = update_parsed_data(new_row)

                except Exception as e:
                    logger.error(
                        f'Error in the refactor_parse_responses function: {e}')
                result.append(new_row)
    return result


def update_parsed_data(
        parse_result: ProfessionParseResponse) -> ProfessionParseResponse:
    """This function updates provided parse_data dictionary
    :param parse_result: a ProfessionParseResponse instance containing parsed
    data to update
    :return: updated ProfessionParseResponse instance
    """
    price = clean_digits(parse_result.price)
    period = clean_digits(parse_result.period)

    try:
        parse_result.price = price
        parse_result.period = period
        parse_result.total = (
            round(price * period) if price and period else parse_result.total)
        parse_result.updated_at = str(datetime.now()).split('.')[0]

    except Exception as e:
        logger.error(
            f'There was an error in the update_parsed_data function: {e}')

    return parse_result


def save_data_to_json(data: Union[dict, list], filename: str) -> None:
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


def convert_parse_tasks_to_json(
        parse_data: list[SchoolParseTask],
        is_convert_request: bool = True) -> dict[str, list[dict]]:
    """This function converts a list of SchoolParseTask instances into
    a dictionary
    :param parse_data: list of SchoolParseTask instances
    :param is_convert_request: boolean indicating if you want to convert
    requests of responses of SchoolParseTask instances
    :return: dictionary containing list of dictionaries
    """
    result = {}
    for task in parse_data:
        if is_convert_request:
            result[task.school_name] = [
                request.dict() for request in
                task.parse_requests
                ]
        else:
            result[task.school_name] = [
                remove_excessive_data(response.dict()) for response in
                task.parse_responses
                ]

    return result


def convert_json_to_parse_tasks(
        data: dict[str, list[dict]]) -> list[SchoolParseTask]:
    """This function converts a dictionary into a list of SchoolParseTask
    instances
    :param data: dictionary containing list of dictionaries
    :return: list of SchoolParseTask instances
    """
    tasks = []
    for key in data:
        new_task = SchoolParseTask()
        new_task.school_name = key
        new_task.parse_requests.extend(
            [ProfessionParseRequest(**task) for task in data[key]])
        tasks.append(new_task)

    return tasks


def compare_data(old_data: dict[str, list],
                 new_data: dict[str, list]) -> dict[str, Any]:
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

            try:
                prof_new['price_change'] = new_price - old_price

            except Exception as e:
                logger.error(f'Cannot calculate price change, error {e}')
                prof_new['price_change'] = 0

            try:
                prof_new['period_change'] = round(new_period - old_period, 2)
            except Exception as e:
                logger.error(f'Cannot calculate period change, error {e}')
                prof_new['period_change'] = 0

            professions.append(prof_new)

        new_data[key] = (
            professions if len(professions) >= len(new_data[key])
            else new_data[key])

    return new_data


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


def refresh_drivers() -> None:
    """This function serves to actualize a chrome driver version"""
    server_pass = os.environ.get('SERVER_PASSWORD')
    subprocess.run(f'echo {server_pass} | sudo -S apt-get update -y && sudo '
                   f'apt-get install google-chrome-stable -y', shell=True)
