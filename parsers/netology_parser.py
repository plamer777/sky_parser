from selenium import webdriver
from selenium.webdriver.common.by import By
from parsers.base_parser import BaseParser
from utils import update_parsed_data


class NetologyParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):

        price, period = self._get_data(parse_data, driver)
        parse_data['price'] = price
        parse_data['period'] = period
        update_parsed_data(parse_data)

        return parse_data

    @staticmethod
    def _get_data(parse_data: dict, driver: webdriver.Chrome):
        driver.get(parse_data.get('url'))

        all_data = driver.find_element(By.CLASS_NAME, parse_data.get(
            'price_tags')[0])

        data_list = all_data.text.split('\n')
        price = data_list[1]
        period = data_list[2].split(' ')[-2]

        return price, period
