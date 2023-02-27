"""This is a main file to start the parser"""
from time import sleep
from constants import RESULT_PATH, SCHOOLS_PATH, TIME_DELAY_24_H
from container import table_manager
from utils import load_from_json
# ------------------------------------------------------------------------


def main() -> None:
    """Main function with necessary logic"""
    while True:
        old_data = load_from_json(RESULT_PATH)
        parse_data = load_from_json(SCHOOLS_PATH)
        table_manager.open_table('sky_parser')
        table_manager.refresh(parse_data, old_data)
        sleep(TIME_DELAY_24_H)


if __name__ == '__main__':
    main()
