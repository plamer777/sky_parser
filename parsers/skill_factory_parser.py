"""This file contains a SkillFactoryParser class to parse SkillFactory site"""
from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class SkillFactoryParser(BaseParser):
    """The SkillFactoryParser class have a logic to parse data from
    SkillFactory site"""
    def parse_data(self, parse_data: dict[str, Any],
                   driver: Chrome) -> dict[str, Any]:
        """This is a main method to parse data from SkillFactory site
        :param parse_data: a dictionary with data to parse containing single
        url and set of tags
        :param driver: a Chrome instance to extract data from html page
        :return: a dictionary containing data from SkillFactory site
        """
        try:
            price, middle_price, pro_price, period = self._get_data(
                parse_data, driver)

            driver.stop_client()
            driver.close()
            parse_data['price'] = price
            parse_data['middle_price'] = middle_price
            parse_data['pro_price'] = pro_price
            parse_data['period'] = period
            logger.info(f'{parse_data.get("url")} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')

        return parse_data

    @staticmethod
    def _get_data(parse_data: dict[str, Any], driver: Chrome) -> tuple:
        """This method extracts data from html page by provided price tags
        :param parse_data: a dictionary with data to parse
        :param driver: a Chrome instance to get html page and extract data
        from it
        :return: a tuple containing data from html page
        """
        driver.get(parse_data.get('url'))

        price = driver.find_element(
            By.XPATH, parse_data.get('price_tags')[0])
        middle_price = driver.find_element(
            By.XPATH, parse_data.get('middle_price_tags')[0])
        pro_price = driver.find_element(
            By.XPATH, parse_data.get('pro_price_tags')[0])
        period = driver.find_element(
            By.XPATH, parse_data.get('period_tags')[0])

        return price.text, middle_price.text, pro_price.text, period.text

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self.parse_data(*args, **kwargs)
