"""This file contains a SkillFactoryParser class to parse SkillFactory site"""
from typing import Union
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from create_loggers import logger
from parse_classes.school_parse_task import ProfessionParseRequest, \
    ProfessionParseResponse
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class SkillFactoryParser(BaseParser):
    """The SkillFactoryParser class have a logic to parse data from
    SkillFactory site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: Chrome
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from SkillFactory site
        :param parse_data: a ProfessionParseRequest instance with data to parse
        containing single url and set of tags
        :param driver: a Chrome instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from
        SkillFactory site or ProfessionParseRequest instance if parsing failed
        """
        parse_response = ProfessionParseResponse.from_orm(parse_data)
        try:
            price, middle_price, pro_price, period = self._get_data(
                parse_data, driver)

            parse_response.price = price
            parse_response.middle_price = middle_price
            parse_response.pro_price = pro_price
            parse_response.period = period
            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.url}, error: {e}')

        finally:
            if driver:
                driver.stop_client()
                driver.quit()

        return parse_response if parse_response.price else parse_data

    @staticmethod
    def _get_data(parse_data: ProfessionParseRequest,
                  driver: Chrome) -> tuple[str, str, str, str]:
        """This method extracts data from html page by provided price tags
        :param parse_data: a ProfessionParseRequest instance with data to parse
        containing single url and set of tags
        :param driver: a Chrome instance to get html page and extract data
        from it
        :return: a tuple containing data from html page
        """
        driver.get(parse_data.url)

        price = driver.find_element(
            By.XPATH, parse_data.price_tags[0])
        middle_price = driver.find_element(
            By.XPATH, parse_data.middle_price_tags[0])
        pro_price = driver.find_element(
            By.XPATH, parse_data.pro_price_tags[0])
        period = driver.find_element(
            By.XPATH, parse_data.period_tags[0])

        return price.text, middle_price.text, pro_price.text, period.text

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
