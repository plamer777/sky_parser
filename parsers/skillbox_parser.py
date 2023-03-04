"""This file contains a SkillBoxParser class to parse SkillBox site"""
from typing import Any
from bs4 import BeautifulSoup
from create_loggers import logger
from parsers.base_parser import BaseParser
from constants import PRICE_TAGS, PRICE_TYPES
# ------------------------------------------------------------------------


class SkillBoxParser(BaseParser):
    """The SkillBoxParser class have a logic to parse data from
    SkillBox site"""
    def parse_data(self, parse_data: dict[str, Any],
                   driver: BeautifulSoup) -> dict[str, Any]:
        """This is a main method to parse data from SkillBox site
        :param parse_data: a dictionary with data to parse containing single
        url and set of tags
        :param driver: a BeautifulSoup instance to extract data from html page
        :return: a dictionary containing data from SkillBox site
        """
        price_tags = parse_data.get('price_tags')
        additional_tags = parse_data.get('additional_price_tags')
        period_tags = parse_data.get('period_tags')

        try:
            for price_type, price_tag in zip(PRICE_TYPES[1:], PRICE_TAGS[1:]):
                if price_tag in parse_data:
                    price_data = str(driver.find(*parse_data[price_tag]))
                    parse_data[price_type] = self.get_from_parsed_data(
                        price_data, additional_tags)

            parse_data['price'] = driver.find(*price_tags).text
            parse_data['period'] = driver.find(*period_tags).text

            parse_data = self._clean_data(parse_data)
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

    @staticmethod
    def _clean_data(data: dict[str, Any]) -> dict[str, Any]:
        """This as an additional method helps to extract parsed data
        :param data: a dictionary with parsed data
        :return: a dictionary with refactored data
        """
        if data.get('profession') == 'Python_developer':
            data['period'] = data['period'].split('.  ')[0]

        elif data.get('profession') in ['Java_developer', 'Data_analyst']:
            pass

        else:
            data['period'] = data['period'].split('Отсрочка платежа')[-2]

        return data

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self.parse_data(*args, **kwargs)
