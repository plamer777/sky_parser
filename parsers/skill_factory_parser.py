from selenium import webdriver
from selenium.webdriver.common.by import By
from parsers.base_parser import BaseParser
from utils import update_parsed_data


class SkillFactoryParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
        price, period = self._get_data(parse_data, driver)
        parse_data['price'] = price
        parse_data['period'] = period
        update_parsed_data(parse_data)

        return parse_data

    @staticmethod
    def _get_data(parse_data: dict, driver: webdriver.Chrome):
        driver.get(parse_data.get('url'))
        price = driver.find_element(By.XPATH, parse_data.get('price_tags')[0])
        period = driver.find_element(By.XPATH, parse_data.get('period_tags')[0])
        return price.text, period.text
