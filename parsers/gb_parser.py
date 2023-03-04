"""This file contains a GBParser class to parse Geek Brains site"""
from typing import Any
from bs4 import BeautifulSoup
from create_loggers import logger
from parsers.base_parser import BaseParser
from constants import PRICE_TYPES
# ------------------------------------------------------------------------


class GBParser(BaseParser):
    """The GBParser class have a logic to parse data from GB site"""
    def parse_data(self, parse_data: dict[str, Any],
                   driver: BeautifulSoup) -> dict[str, Any]:
        """This is a main method to parse data from GB site
        :param parse_data: a dictionary with data to parse containing single
        url and set of tags
        :param driver: a BeautifulSoup instance to extract data from html page
        :return: a dictionary containing data from GB site
        """
        price_tags = parse_data.get('price_tags')
        period_tags = parse_data.get('period_tags')

        try:
            all_prices = driver.find_all(*price_tags)
            for index, price in enumerate(PRICE_TYPES):
                if price in parse_data:
                    parse_data[price] = all_prices[index].text

            parse_data['period'] = driver.find(*period_tags).text
            logger.info(f'{parse_data.get("url")} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')

        return parse_data

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self.parse_data(*args, **kwargs)
