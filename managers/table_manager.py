from gspread import Client
from constants import RESULT_PATH, TITLES
from managers.parse_manager import ParseManager
from utils import compare_data, remove_excessive_data, save_data_to_json
# ------------------------------------------------------------------------


class GoogleTableManager:
    """GoogleTableManager class provides all necessary logic to send parsed
    data to the Google sheets"""
    def __init__(self, connection: Client, parse_manager: ParseManager):
        self.connection = connection
        self.table = None
        self.parse_manager = parse_manager

    def open_table(self, table_name: str):
        self.table = self.connection.open(table_name)

    def refresh(self, parse_data: dict[str, list], old_data: dict[str, list]):
        data = self.parse_manager.parse_all(parse_data)
        cleaned = remove_excessive_data(data)
        updated = compare_data(old_data, cleaned)
        save_data_to_json(updated, RESULT_PATH)

        records = [TITLES]
        for key in updated:
            for row in data[key]:

                row_list = list(row.values())
                row_list.insert(0, key)
                records.append(row_list)

        self.table.sheet1.clear()
        self.table.sheet1.update(records)
