from parsers.base_parser import BaseParser
from utils import update_parsed_data


class GBParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
        price_tags = parse_data.get('price_tags')
        period_tags = parse_data.get('period_tags')
        parse_data['price'] = driver.find(*price_tags).text
        parse_data['period'] = driver.find(*period_tags).text
        result = update_parsed_data(parse_data)
        return result
