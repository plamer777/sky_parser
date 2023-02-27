from bs4 import BeautifulSoup
from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class GBParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
        price_tags = parse_data.get('price_tags')
        middle_price_tags = parse_data.get('middle_price_tags')
        pro_price_tags = parse_data.get('pro_price_tags')
        additional_price_tags = parse_data.get('additional_price_tags')
        period_tags = parse_data.get('period_tags')

        try:
            if middle_price_tags:
                middle_price_tags = driver.find(*middle_price_tags)
                middle_price = self.get_from_parsed_data(middle_price_tags,
                                                         additional_price_tags)
                parse_data['middle_price'] = middle_price

            if pro_price_tags:
                pro_price_tags = driver.find(*pro_price_tags)
                pro_price = self.get_from_parsed_data(pro_price_tags,
                                                      additional_price_tags)
                parse_data['pro_price'] = pro_price

            parse_data['price'] = driver.find(*price_tags).text
            parse_data['period'] = driver.find(*period_tags).text
            logger.info(f'{parse_data.get("url")} parsed successfully')
        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')

        return parse_data

    @staticmethod
    def get_from_parsed_data(parsed_data, additional_tags):

        sup = BeautifulSoup(str(parsed_data), 'html.parser')
        result = sup.find(*additional_tags).text

        return result
