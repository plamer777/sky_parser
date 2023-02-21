from parsers.gb_parser import GBParser
from parsers.netology_parser import NetologyParser
from parsers.skill_factory_parser import SkillFactoryParser
from managers.parse_manager import ParseManager
from parsers.skillbox_parser import SkillBoxParser
from parsers.yandex_parser import YandexPracticumParser
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
