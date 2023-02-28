"""This file contains a NetologyParser class to parse Netology site"""
from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class NetologyParser(BaseParser):
    """The NetologyParser class have a logic to parse data from
    Netology site"""
    def parse_data(self, parse_data: dict[str, Any],
                   driver: Chrome) -> dict[str, Any]:
        """This is a main method to parse data from Netology site
        :param parse_data: a dictionary with data to parse containing single
        url and set of tags
        :param driver: a Chrome instance to extract data from html page
        :return: a dictionary containing data from Netology site
        """
        try:
            price, period = self._get_data(parse_data, driver)
            driver.stop_client()
            driver.close()
            parse_data['price'] = price
            parse_data['period'] = period
            logger.info(f'{parse_data.get("url")} parsed successfully')

        except Exception as e:
            logger.error(
                f'Failed to parse {parse_data.get("url")}, error: {e}')

        return parse_data

    @staticmethod
    def _get_data(parse_data: dict,
                  driver: Chrome) -> tuple[str, str]:
        """This method extracts data from html page by provided price tags
        :param parse_data: a dictionary with data to parse
        :param driver: a Chrome instance to get html page and extract data
        from it
        :return: a tuple containing data from html page
        """
        driver.get(parse_data.get('url'))

        all_data = driver.find_element(By.CLASS_NAME, parse_data.get(
            'price_tags')[0])

        data_list = all_data.text.split('\n')
        price = data_list[1]
        period = data_list[2].split(' ')[-2]

        return price, period

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self.parse_data(*args, **kwargs)