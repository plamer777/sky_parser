"""This is a main file to start the parser"""
from time import sleep
from datetime import datetime
from constants import RESULT_PATH, TIME_DELAY_24_H, TABLE_NAME, \
    PARSE_TAGS_SHEET
from container import table_manager
from utils import load_from_json
# ------------------------------------------------------------------------


def main() -> None:
    """Main function with necessary logic"""
    while True:
        start_time = datetime.now()

        table_manager.open_table(TABLE_NAME)
        parse_data = table_manager.load_from_table(PARSE_TAGS_SHEET)

        old_data = load_from_json(RESULT_PATH)

        table_manager.refresh(parse_data, old_data)
        table_manager.close_table()

        work_time = (datetime.now() - start_time).seconds
        sleep(TIME_DELAY_24_H - work_time)


if __name__ == '__main__':
    main()



