"""This file contains a YandexPracticumParser class to parse
YandexPracticum site"""
from typing import Union, Optional
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from create_loggers import logger
from parse_classes.school_parse_task import ProfessionParseRequest, \
    ProfessionParseResponse
from parsers.base_parser import BaseParser
from utils import clean_digits
# ------------------------------------------------------------------------


class YandexPracticumParser(BaseParser):
    """The YandexPracticumParser class have a logic to parse data from
    YandexPracticum site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: Chrome
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from YandexPracticum site
        :param parse_data: a ProfessionParseRequest instance with data to parse
        containing single url and set of tags
        :param driver: a Chrome instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from
        YandexPracticum site or ProfessionParseRequest instance if parsing
        failed
        """
        result = self._load_data(parse_data, driver)
        driver.stop_client()
        driver.close()

        if not result:
            return parse_data

        return result

    def _load_data(
            self, parse_data: ProfessionParseRequest,
            driver: Chrome) -> Optional[ProfessionParseResponse]:
        """This is a main method to load html page from YandexPracticum and
        extract necessary data
        :param parse_data: a ProfessionParseRequest instance with data to parse
        :param driver: a Chrome instance to load data from html page
        :return: a dictionary containing data from YandexPracticum
        """
        try:
            driver.get(parse_data.url)
            sup = BeautifulSoup(driver.page_source, 'html.parser')
            result = self._filter_data(parse_data, sup)
            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.url}, error: {e}')
            return None

        return result

    @staticmethod
    def _filter_data(data: ProfessionParseRequest,
                     sup: BeautifulSoup) -> ProfessionParseResponse:
        """This method helps extract data from previously loaded html page
        by using BeautifulSoup
        :param data: an instance of ProfessionParseRequest with data to parse
        :param sup: a configured BeautifulSoup instance with loaded html page
        :return: a ProfessionParseResponse instance containing extracted data
        """
        price_data = sup.find(*data.price_tags)
        parse_response = ProfessionParseResponse.from_orm(data)
        if not price_data:
            raise ValueError

        profession = data.profession
        if profession in ['Java_developer', 'Graphic_designer',
                          'Internet_marketer']:
            price, period = price_data.text.split('на')[:2]

        else:
            total_price = sup.find(*data.total_tags)
            price_data = sup.find_all(*data.price_tags)

            if getattr(data, 'pro_price_tags', None):
                parse_response.pro_price = price_data[-2].text

            parse_response.middle_price = price_data[-1].text

            price = clean_digits(price_data[0].text)
            total = clean_digits(total_price.text)
            period = round(total / price, 2)

        parse_response.period = period
        parse_response.price = str(price)

        return parse_response

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
