"""This file contains different constants such as file paths, table names,
etc."""
import os
# ------------------------------------------------------------------------

PARSE_DATA_PATH = os.path.join('data', 'parse_store')
RESULT_PATH = os.path.join('data', 'results', 'result.json')
AUTH_FILE = os.path.join('auth_data', 'skyparser-b7b18db49e8d.json')
LOG_PATH = os.path.join('log', 'parser_logs.txt')
BOT_PHRASES_PATH = os.path.join('data', 'telebot_data', 'bot_phrases.json')
CHAT_IDS_PATH = os.path.join('data', 'telebot_data', 'chats.json')

TIME_DELAY_24_H = 3600 * 24

MULTY_THREAD_ATTEMPTS = 30
ASYNC_ATTEMPTS = 10


TABLE_NAME = 'sky_parser'
PARSE_TAGS_SHEET = 'Парсинг теги'
HISTORY_SHEET = 'История'
RESULT_SHEET = 'Парсинг'


TITLES = ['school',
          'profession',
          'course_level',
          'price per month',
          'period',
          'total price',
          'price change',
          'period change',
          'url',
          'updated'
          ]

LOG_FORMAT_STR = '[%(levelname)s] - [%(asctime)s] :' \
                 ' <%(message)s> : str№: %(lineno)s'

PRICE_TAGS = ('price_tags',
              'middle_price_tags',
              'pro_price_tags'
              )

REFACTOR_TAGS = PRICE_TAGS + (
    'additional_price_tags'
    'total_tags',
    'period_tags',
    'url',
)

PRICE_TYPES = ('price', 'middle_price', 'pro_price')

PERIODS = {
    'price': 'period',
    'middle_price': 'middle_period',
    'pro_price': 'pro_period'
}

LEVELS = {
    'price': 'basic',
    'middle_price': 'middle',
    'pro_price': 'pro'
}

PRICE_LEVELS = {
    'price_tags': 'price',
    'middle_price_tags': 'middle_price',
    'pro_price_tags': 'pro_price',
    'total_tags': 'total',
    'period_tags': 'period',
}

SERVICE_TAGS = ('price_tags',
                'period_tags',
                'total_tags',
                'additional_price_tags',
                'middle_price_tags',
                'pro_price_tags',
                'pro_price',
                'middle_price',
                'middle_period',
                'pro_period')

INITIAL_PARSE_DATA = {
      "price": "",
      "period": "",
      "total": ""
    }
