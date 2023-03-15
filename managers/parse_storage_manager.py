"""This file contains the ParseStoreManager class created to save and
download parse data in the storage for reservation"""
import os
from typing import Optional
from create_loggers import logger
from parse_classes.school_parse_task import SchoolParseTask
from utils import (save_data_to_json, load_from_json,
                   convert_json_to_parse_tasks, convert_parse_tasks_to_json)
# --------------------------------------------------------------------------


class ParseStorageManager:
    """The ParseStorageManager class provides a mechanism for storing and
    downloading parse data"""
    def __init__(self, storage_path: str) -> None:
        """Initialize the ParseStorageManager class
        :param storage_path: a string containing the path to the storage
        directory
        """
        self._current_file_version: int = 0
        self._storage_path: str = storage_path

    def save_to_storage(
            self, parse_data: list[SchoolParseTask],
            max_files: int = 10) -> None:
        """This method is called to save the parse data to the storage
        :param parse_data: a list of SchoolParseTask instances
        :param max_files: the maximum amount of files to store
        """
        result = convert_parse_tasks_to_json(parse_data)
        if self._current_file_version > max_files - 1:
            self._current_file_version = 0

        file_path = os.path.join(
            self._storage_path, f'save{self._current_file_version}.json')
        save_data_to_json(result, file_path)
        self._current_file_version += 1

    def load_from_storage(
            self, version: int = None) -> Optional[list[SchoolParseTask]]:
        """This method is called to load the parse data from the storage in
        case of the data was removed from the Google Sheet or the sheet is
        unavailable
        :param version: the version of the file to load
        :return: a list of SchoolParseTask instances or None if the file
        cannot be loaded
        """
        try:
            all_files = next(os.walk(self._storage_path))[2]
            if self._current_file_version < len(all_files):
                self._current_file_version = len(all_files) - 1

            if version is None or type(version) is not int:
                version = self._current_file_version

            while version >= self._current_file_version:
                parse_file = os.path.join(
                    self._storage_path, f'save{version}.json')
                parse_data = load_from_json(parse_file)

                if parse_data:
                    return convert_json_to_parse_tasks(parse_data)
                version -= 1

        except Exception as e:
            logger.error(f'Failed to load data from {self._storage_path}, '
                         f'error {e}')

        return None
