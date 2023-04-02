from os import environ
import dotenv
import gspread
from telebot.async_telebot import AsyncTeleBot
from constants import AUTH_FILE, PARSE_DATA_PATH, RESULT_PATH
from managers import (ParseStorageManager, ParseManager,
                      GoogleTableManager, DataManager, TelebotManager)
from parsers import (GBParser, NetologyParser, SkillFactoryParser,
                     SkillBoxParser, YandexPracticumParser)
# ------------------------------------------------------------------------
dotenv.load_dotenv()
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

chat_ids = set()

parse_manager = ParseManager(parsers, parse_mapper)
connection = gspread.service_account(AUTH_FILE)
table_manager = GoogleTableManager(connection, parse_manager)
storage_manager = ParseStorageManager(PARSE_DATA_PATH)
data_manager = DataManager(RESULT_PATH)

bot = AsyncTeleBot(environ.get('BOT_TOKEN'))
telebot_manager = TelebotManager(bot)
