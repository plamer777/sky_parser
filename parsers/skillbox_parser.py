"""This file contains a SkillBoxParser class to parse SkillBox site"""
from typing import Union
from bs4 import BeautifulSoup
from create_loggers import logger
from parse_classes.school_parse_task import (
    ProfessionParseResponse, ProfessionParseRequest)
from parsers.base_parser import BaseParser
from constants import PRICE_TAGS, PRICE_TYPES
# ------------------------------------------------------------------------


class SkillBoxParser(BaseParser):
    """The SkillBoxParser class have a logic to parse data from
    SkillBox site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: BeautifulSoup
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from SkillBox site
        :param parse_data: a ProfessionParseRequest instance with data to parse
        containing single url and set of tags
        :param driver: a BeautifulSoup instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from
        SkillBox site or ProfessionParseRequest instance if parsing failed
        """
        price_tags = parse_data.price_tags
        period_tags = parse_data.period_tags
        parse_response = ProfessionParseResponse.from_orm(parse_data)

        try:
            prices = driver.find_all(*price_tags)
            periods = driver.find_all(*period_tags)
            parse_response = self._sort_extracted_data(
                parse_response, parse_data, prices, periods)

            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.url}, error: {e}')

        return parse_response if parse_response.price else parse_data

    @staticmethod
    def _sort_extracted_data(
            parse_response: ProfessionParseResponse,
            parse_request: ProfessionParseRequest,
            prices: list, periods: list) -> ProfessionParseResponse:
        """This as an additional method helps to sort parsed data by the
        profession, course type (basic, middle, pro) etc.
        :param parse_response: a ProfessionParseResponse instance with
        parsed data
        :param parse_request: a ProfessionParseRequest instance with
        necessary tags
        :param prices: a list of strings representing parsed prices
        :param periods: a list of strings representing parsed periods
        :return: a ProfessionParseResponse instance with refactored data
        """

        if parse_response.profession == 'Python_developer':
            parse_response.period = periods[0].text.split('месяц')[0] or ''

        elif parse_response.profession in ('Graphic_designer',):
            parse_response.period = periods[1].text or ''

        else:
            parse_response.period = periods[0].text or ''

        for index, (price_type, price_tag) in enumerate(
                zip(PRICE_TYPES, PRICE_TAGS)):
            if getattr(parse_request, price_tag, None):
                setattr(parse_response, price_type, prices[index].text or '')

        return parse_response

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
