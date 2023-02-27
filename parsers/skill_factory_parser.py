from selenium import webdriver
from selenium.webdriver.common.by import By
from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class SkillFactoryParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
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
    def _get_data(parse_data: dict, driver: webdriver.Chrome):

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
