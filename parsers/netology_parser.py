"""This file contains a NetologyParser class to parse Netology site"""
from typing import Union
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from create_loggers import logger
from parse_classes.school_parse_task import ProfessionParseRequest, \
    ProfessionParseResponse
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class NetologyParser(BaseParser):
    """The NetologyParser class have a logic to parse data from
    Netology site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: Chrome
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from Netology site
        :param parse_data: a ProfessionParseRequest instance containing single
        url and set of tags
        :param driver: a Chrome instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from
        Netology site or ProfessionParseRequest instance if parsing failed
        """
        parse_response = ProfessionParseResponse.from_orm(parse_data)
        try:
            price, period = self._get_data(parse_data, driver)
            parse_response.price = price
            parse_response.period = period
            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Failed to parse {parse_data.url}, error: {e}')

        driver.stop_client()
        driver.close()
        return parse_response if parse_response.price else parse_data

    @staticmethod
    def _get_data(parse_data: ProfessionParseRequest,
                  driver: Chrome) -> tuple[str, str]:
        """This method extracts data from html page by provided price tags
        :param parse_data: a ProfessionParseRequest instance with data to parse
        :param driver: a Chrome instance to get html page and extract data
        from it
        :return: a tuple containing data from html page
        """
        driver.get(parse_data.url)

        all_data = driver.find_element(By.CLASS_NAME, parse_data.price_tags[0])

        data_list = all_data.text.split('\n')
        price = data_list[1]
        period = data_list[2].split(' ')[-2]

        return price, period

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
