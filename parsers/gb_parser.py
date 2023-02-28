"""This file contains a GBParser class to parse Geek Brains site"""
from typing import Any
from bs4 import BeautifulSoup, Tag
from create_loggers import logger
from parsers.base_parser import BaseParser
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
        middle_price_tags = parse_data.get('middle_price_tags')
        pro_price_tags = parse_data.get('pro_price_tags')
        additional_price_tags = parse_data.get('additional_price_tags')
        period_tags = parse_data.get('period_tags')

        try:
            if middle_price_tags:
                middle_price_tags = str(driver.find(*middle_price_tags))
                middle_price = self.get_from_parsed_data(middle_price_tags,
                                                         additional_price_tags)
                parse_data['middle_price'] = middle_price

            if pro_price_tags:
                pro_price_tags = str(driver.find(*pro_price_tags))
                pro_price = self.get_from_parsed_data(pro_price_tags,
                                                      additional_price_tags)
                parse_data['pro_price'] = pro_price

            parse_data['price'] = driver.find(*price_tags).text
            parse_data['period'] = driver.find(*period_tags).text
            logger.info(f'{parse_data.get("url")} parsed successfully')
        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')

        return parse_data

    @staticmethod
    def get_from_parsed_data(parsed_data: str,
                             additional_tags: list[str]) -> str:
        """This method serves to extract data from previously parsed
        :param parsed_data: a string representing a part of the
        html document
        :param additional_tags: a list of strings representing tags to
        extract from the parsed data
        :return: a string containing the extracted data
        """
        sup = BeautifulSoup(parsed_data, 'html.parser')
        result = sup.find(*additional_tags).text

        return result

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self.parse_data(*args, **kwargs)
