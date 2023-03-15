"""This file contains GoogleTableManager to send parsed data to
Google Sheets"""
from typing import Any, Optional
from gspread import Client, Spreadsheet
from constants import RESULT_PATH, TITLES, HISTORY_SHEET, RESULT_SHEET
from create_loggers import logger
from managers.parse_manager import ParseManager
from parse_classes.school_parse_task import SchoolParseTask
from utils import (compare_data, save_data_to_json,
                   convert_table_data_to_parse_tasks,
                   convert_parse_tasks_to_json,
                   refactor_parse_tags)
# ------------------------------------------------------------------------


class GoogleTableManager:
    """GoogleTableManager class provides all necessary logic to send parsed
    data to the Google sheets"""
    def __init__(
            self, connection: Client, parse_manager: ParseManager) -> None:
        """Initialization of the GoogleTableManager class
        :param connection: a Client instance to get access to the
        Google Sheets
        :param parse_manager: a ParseManager instance
        """
        self._connection = connection
        self._table: Optional[Spreadsheet] = None
        self._parse_manager = parse_manager

    def open_table(self, table_name: str) -> None:
        """This method serves to open a table by provided name
        :param table_name: a name of the table to open
        """
        self._table = self._connection.open(table_name)

    def close_table(self) -> None:
        """This method serves to close previously opened table"""
        self._connection.session.close()

    def refresh(self, parse_data: list[SchoolParseTask],
                old_data: dict[str, list] = None) -> None:
        """This is a main method to start parsing process and send parsed
        data to the Google Sheets
        :param parse_data: a dictionary with data to be parsed such as urls,
        tags, etc.
        :param old_data: a dictionary with previously parsed data
        """
        try:
            finished_tasks = self._parse_manager.parse_all(parse_data)
            new_parse_data = convert_parse_tasks_to_json(finished_tasks, False)
            if old_data:
                new_parse_data = compare_data(old_data, new_parse_data)
            save_data_to_json(new_parse_data, RESULT_PATH)

            records = [TITLES]
            for key in new_parse_data:
                for row in new_parse_data[key]:
                    row['school'] = key
                    row_list = self._create_row(row)
                    records.append(row_list)

            self._table.worksheet(RESULT_SHEET).update(records)
            records[0] = []
            self._table.worksheet(HISTORY_SHEET).append_rows(records)
            logger.info(f'Table refreshed successfully')

        except Exception as e:
            logger.error(
                f'There was an error while refreshing the table: {e}')

    @staticmethod
    def _create_row(data: dict[str, Any]) -> list:
        """This secondary method serves to generate a row for Google Sheets
        in the certain order
        :param data: a dictionary with parsed data to create the row
        :return: a list containing the parsed data in the certain order
        """
        row = [data['school'], data['profession'], data['course_level'],
               data['price'], data['period'], data['total'],
               data['price_change'], data['period_change'],
               data['url'], data['updated_at']
               ]

        return row

    def load_from_table(
            self, table_name: str) -> Optional[list[SchoolParseTask]]:
        """This method is used to load data from GoogleSheets and convert it
        to dictionary containing lists of dictionaries
        :param table_name: the name of the sheet to load data from
        :return: a list of SchoolParseTask instances containing the
        parse requests
        """
        try:
            raw_parse_data = self._table.worksheet(table_name).get_all_values()
            parse_data = convert_table_data_to_parse_tasks(raw_parse_data)
        except Exception as e:
            logger.error(f'Failed to load data from {table_name}, error: {e}')
            parse_data = []

        return parse_data

    def send_from_json_to_table(self, json_data: dict[str, list],
                                table_name: str) -> None:
        """This method is used to send data to GoogleSheets
        :param json_data: dictionary containing parse data
        :param table_name: the name of the sheet to send data to
        """
        refactored_data = self._convert_json_to_table_data(json_data)
        self._table.worksheet(table_name).update(refactored_data)

    @staticmethod
    def _convert_json_to_table_data(data: dict[str, list]) -> list[list]:
        """This method converts dictionary with parse data into a list of lists
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
