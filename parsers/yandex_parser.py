from selenium import webdriver
from bs4 import BeautifulSoup
from create_loggers import logger
from parsers.base_parser import BaseParser
from utils import clean_digits
# ------------------------------------------------------------------------


class YandexPracticumParser(BaseParser):

    def parse_data(self, parse_data: dict, driver: webdriver.Chrome):

        result = self._load_data(parse_data, driver)
        driver.stop_client()
        driver.quit()

        if not result:
            return parse_data

        return result

    def _load_data(self, parse_data: dict, driver: webdriver.Chrome) -> dict:

        try:
            driver.get(parse_data.get('url'))
            sup = BeautifulSoup(driver.page_source, 'html.parser')
            result = self._filter_data(parse_data, sup)
            logger.info(f'{parse_data.get("url")} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')
            return {}

        return result

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
            price_data = sup.find_all(*data.get('price_tags'))
            if 'pro_price_tags' in data:
                data['pro_price'] = price_data[-2].text

            data['middle_price'] = price_data[-1].text

            price = clean_digits(price_data[0].text)
            total = clean_digits(total_price.text)
            period = round(total / price, 2)

        data['period'] = period
        data['price'] = str(price)

        return data
