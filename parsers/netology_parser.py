from selenium import webdriver
from selenium.webdriver.common.by import By
from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class NetologyParser(BaseParser):

    def parse_data(self, parse_data: dict, driver: webdriver.Chrome):

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
    def _get_data(parse_data: dict, driver: webdriver.Chrome):
        driver.get(parse_data.get('url'))

        all_data = driver.find_element(By.CLASS_NAME, parse_data.get(
            'price_tags')[0])

        data_list = all_data.text.split('\n')
        price = data_list[1]
        period = data_list[2].split(' ')[-2]

        return price, period
