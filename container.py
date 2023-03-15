import gspread
from constants import AUTH_FILE, PARSE_DATA_PATH
from managers.parse_storage_manager import ParseStorageManager
from parsers.gb_parser import GBParser
from parsers.netology_parser import NetologyParser
from parsers.skill_factory_parser import SkillFactoryParser
from managers.parse_manager import ParseManager
from parsers.skillbox_parser import SkillBoxParser
from parsers.yandex_parser import YandexPracticumParser
from managers.table_manager import GoogleTableManager
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
