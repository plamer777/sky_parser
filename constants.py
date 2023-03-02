"""This file contains different constants such as file paths, table names,
etc."""
import os
# ------------------------------------------------------------------------

SCHOOLS_PATH = os.path.join('data', 'schools_new.json')
RESULT_PATH = os.path.join('data', 'result.json')
AUTH_FILE = os.path.join('auth_data', 'skyparser-b7b18db49e8d.json')
DRIVER_PATH = os.path.join('driver', 'chromedriver')
LOG_PATH = os.path.join('log', 'parser_logs.txt')

TIME_DELAY_24_H = 3600 * 24


HISTORY_TABLE = 'История'
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


PRICE_TYPES = ('price', 'middle_price', 'pro_price')
LEVELS = {'price': 'basic',
          'middle_price': 'middle',
          'pro_price': 'pro'}

SERVICE_TAGS = ('price_tags',
                'period_tags',
                'total_tags',
                'additional_price_tags',
                'middle_price_tags',
                'pro_price_tags',
                'pro_price',
                'middle_price')
