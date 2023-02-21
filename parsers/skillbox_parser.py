from parsers.base_parser import BaseParser
from utils import update_parsed_data
# ------------------------------------------------------------------------


class SkillBoxParser(BaseParser):

    def parse_data(self, parse_data: dict, driver):
        price_tags = parse_data.get('price_tags')
        period_tags = parse_data.get('period_tags')
        parse_data['price'] = driver.find(*price_tags).text
        parse_data['period'] = driver.find(*period_tags).text

        parse_data = self._clean_data(parse_data)

        result = update_parsed_data(parse_data)
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

