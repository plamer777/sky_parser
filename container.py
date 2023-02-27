import gspread
from constants import AUTH_FILE
from parsers.gb_parser import GBParser
from parsers.netology_parser import NetologyParser
from parsers.skill_factory_parser import SkillFactoryParser
from managers.parse_manager import ParseManager
from parsers.skillbox_parser import SkillBoxParser
from parsers.yandex_parser import YandexPracticumParser
from managers.table_manager import GoogleTableManager
# ------------------------------------------------------------------------

parsers = {
    'GeekBrains': GBParser().parse_data,
    'Netology': NetologyParser().parse_data,
    'SkillFactory': SkillFactoryParser().parse_data,
    'SkillBox': SkillBoxParser().parse_data,
    'YandexPracticum': YandexPracticumParser().parse_data,
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
