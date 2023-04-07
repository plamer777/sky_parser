"""This file contains different utility functions to load and save data,
refactor dictionaries, etc."""
import json
from typing import Union
from create_loggers import logger
# ------------------------------------------------------------------------


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
