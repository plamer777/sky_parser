from bs4 import BeautifulSoup

from create_loggers import logger
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


class SkillBoxParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
        price_tags = parse_data.get('price_tags')
        middle_price_tags = parse_data.get('middle_price_tags')
        pro_price_tags = parse_data.get('pro_price_tags')
        additional_tags = parse_data.get('additional_price_tags')

        try:
            if middle_price_tags:
                middle_price_data = str(driver.find(*middle_price_tags))

                parse_data['middle_price'] = self.get_from_parsed_data(
                    middle_price_data, additional_tags)

            if pro_price_tags:
                pro_price_data = str(driver.find(*pro_price_tags))
                parse_data['pro_price'] = self.get_from_parsed_data(
                    pro_price_data, additional_tags)

            period_tags = parse_data.get('period_tags')
            parse_data['price'] = driver.find(*price_tags).text
            parse_data['period'] = driver.find(*period_tags).text

            parse_data = self._clean_data(parse_data)
            logger.info(f'{parse_data.get("url")} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.get("url")}, error: {e}')

        return parse_data

    @staticmethod
    def get_from_parsed_data(parsed_data: str, additional_tags: list):
        sup = BeautifulSoup(parsed_data, 'html.parser')
        result = sup.find(*additional_tags).text
        return result

    @staticmethod
    def _clean_data(data: dict):
        if data.get('profession') == 'Python_developer':
            data['period'] = data['period'].split('.  ')[0]

        elif data.get('profession') in ['Java_developer', 'Data_analyst']:
            pass

        else:
            data['period'] = data['period'].split('  ')[-3]

        return data

