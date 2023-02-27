from typing import Any
from gspread import Client
from constants import RESULT_PATH, TITLES, HISTORY_TABLE
from create_loggers import logger
from managers.parse_manager import ParseManager
from utils import compare_data, remove_excessive_data, save_data_to_json
# ------------------------------------------------------------------------


class GoogleTableManager:
    """GoogleTableManager class provides all necessary logic to send parsed
    data to the Google sheets"""
    def __init__(self, connection: Client, parse_manager: ParseManager):
        self._connection = connection
        self._table = None
        self._parse_manager = parse_manager

    def open_table(self, table_name: str):
        self._table = self._connection.open(table_name)

    def refresh(self, parse_data: dict[str, list], old_data: dict[str, list]):
        try:
            data = self._parse_manager.parse_all(parse_data)
            cleaned = remove_excessive_data(data)
            if old_data:
                cleaned = compare_data(old_data, cleaned)
            save_data_to_json(cleaned, RESULT_PATH)

            records = [TITLES]
            for key in cleaned:
                for row in data[key]:
                    row_list = self._create_row(key, row)
                    records.append(row_list)

            self._table.sheet1.update(records)
            records[0] = []
            self._table.worksheet(HISTORY_TABLE).append_rows(records)
            logger.info(f'Table refreshed successfully')

        except Exception as e:
            logger.error(
                f'There was an error while refreshing the table: {e}')

    @staticmethod
    def _create_row(first_field: str, data: dict[str, Any]):

        row = [first_field, data['profession'], data['course_level'],
               data['price'], data['period'], data['total'],
               data['price_change'], data['price_change'],
               data['url'], data['updated_at']
               ]

        return row
