"""This file contains a GBParser class to parse Geek Brains site"""
from typing import Union
from bs4 import BeautifulSoup
from create_loggers import logger
from parse_classes.school_parse_task import ProfessionParseRequest, \
    ProfessionParseResponse
from parsers.base_parser import BaseParser
from constants import PRICE_TAGS, PRICE_LEVELS
# ------------------------------------------------------------------------


class GBParser(BaseParser):
    """The GBParser class have a logic to parse data from GB site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: BeautifulSoup
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from GB site
        :param parse_data: a ProfessionParseRequest instance
        containing single url and set of tags
        :param driver: a BeautifulSoup instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from GB
        site
        """
        price_tags = parse_data.price_tags
        period_tags = parse_data.period_tags
        parse_response = ProfessionParseResponse.from_orm(parse_data)

        try:
            all_prices = driver.find_all(*price_tags)

            for index, tag in enumerate(PRICE_TAGS):
                if getattr(parse_data, tag, None):
                    setattr(parse_response, PRICE_LEVELS[tag],
                            all_prices[index].text)

            parse_response.period = driver.find(*period_tags).text
            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.url}, error: {e}')

        return parse_response if parse_response.price else parse_data

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
