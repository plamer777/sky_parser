from selenium import webdriver
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser
from utils import update_parsed_data, clean_digits
# ------------------------------------------------------------------------


class YandexPracticumParser(BaseParser):

    def parse_data(self, parse_data: dict, driver: webdriver.Chrome):

        price, period = self._load_data(parse_data, driver)
        driver.quit()

        if not price:
            return parse_data

        parse_data['price'] = price
        parse_data['period'] = period
        update_parsed_data(parse_data)

        return parse_data

    def _load_data(self, parse_data: dict, driver: webdriver.Chrome):

        try:
            driver.get(parse_data.get('url'))
            sup = BeautifulSoup(driver.page_source, 'html.parser')
            price, period = self._filter_data(parse_data, sup)

        except Exception:
            return None, None

        return str(price), str(period)

    @staticmethod
    def _filter_data(data: dict, sup: BeautifulSoup):

        price_data = sup.find(*data.get('price_tags'))
        if not price_data:
            raise ValueError

        profession = data.get('profession')
        if profession in ['Java_developer', 'Graphic_designer',
                          'Internet_marketer']:

            data_list = price_data.text.split('на')
            price = data_list[0]
            period = data_list[1]

        else:
            total_price = sup.find(*data.get('total_tags'))
            price = clean_digits(price_data.text)
            total = clean_digits(total_price.text)
            period = round(total / price)

        return price, period
