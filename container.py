import gspread
from constants import AUTH_FILE, PARSE_DATA_PATH
from managers import ParseStorageManager, ParseManager, GoogleTableManager
from parsers import (GBParser, NetologyParser, SkillFactoryParser,
                     SkillBoxParser, YandexPracticumParser)
# ------------------------------------------------------------------------


parsers = {
    'GeekBrains': GBParser(),
    'Netology': NetologyParser(),
    'SkillFactory': SkillFactoryParser(),
    'SkillBox': SkillBoxParser(),
    'YandexPracticum': YandexPracticumParser(),
}

parse_mapper = {
    'GeekBrains': 'async',
    'Netology': 'sync',
    'SkillFactory': 'sync',
    'SkillBox': 'async',
    'YandexPracticum': 'sync',
}

parse_manager = ParseManager(parsers, parse_mapper)
connection = gspread.service_account(AUTH_FILE)
table_manager = GoogleTableManager(connection, parse_manager)
storage_manager = ParseStorageManager(PARSE_DATA_PATH)
