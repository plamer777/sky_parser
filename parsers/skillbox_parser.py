"""This file contains a SkillBoxParser class to parse SkillBox site"""
from typing import Union
from bs4 import BeautifulSoup
from create_loggers import logger
from parse_classes.school_parse_task import ProfessionParseResponse, \
    ProfessionParseRequest
from parsers.base_parser import BaseParser
from constants import PRICE_TAGS, PRICE_TYPES
# ------------------------------------------------------------------------


class SkillBoxParser(BaseParser):
    """The SkillBoxParser class have a logic to parse data from
    SkillBox site"""
    def _parse_data(
            self, parse_data: ProfessionParseRequest,
            driver: BeautifulSoup
    ) -> Union[ProfessionParseResponse, ProfessionParseRequest]:
        """This is a main method to parse data from SkillBox site
        :param parse_data: a ProfessionParseRequest instance with data to parse
        containing single url and set of tags
        :param driver: a BeautifulSoup instance to extract data from html page
        :return: a ProfessionParseResponse instance containing data from
        SkillBox site or ProfessionParseRequest instance if parsing failed
        """
        price_tags = parse_data.price_tags
        additional_tags = parse_data.additional_price_tags
        period_tags = parse_data.period_tags
        parse_response = ProfessionParseResponse.from_orm(parse_data)

        try:
            for price_type, price_tag in zip(PRICE_TYPES[1:], PRICE_TAGS[1:]):
                if getattr(parse_data, price_tag, None):
                    price_data = str(
                        driver.find(*getattr(parse_data, price_tag)))
                    setattr(
                        parse_response, price_type,
                        self._get_from_parsed_data(price_data, additional_tags)
                    )

            parse_response.price = driver.find(*price_tags).text
            parse_response.period = driver.find(*period_tags).text

            parse_data = self._clean_data(parse_response)
            logger.info(f'{parse_data.url} parsed successfully')

        except Exception as e:
            logger.error(
                f'Could not parse {parse_data.url}, error: {e}')

        return parse_response if parse_response.price else parse_data

    @staticmethod
    def _get_from_parsed_data(parsed_data: str,
                              additional_tags: list[str]) -> str:
        """This method serves to extract data from previously parsed one
        :param parsed_data: a string representing a part of the
        html document
        :param additional_tags: a list of strings representing tags to
        extract from the parsed data
        :return: a string containing the extracted data
        """
        sup = BeautifulSoup(parsed_data, 'html.parser')
        result = sup.find(*additional_tags).text
        return result

    @staticmethod
    def _clean_data(data: ProfessionParseResponse) -> ProfessionParseResponse:
        """This as an additional method helps to extract parsed data
        :param data: a ProfessionParseResponse instance with parsed data
        :return: a ProfessionParseResponse instance with refactored data
        """
        if data.profession == 'Python_developer':
            data.period = data.period.split('.')[0]

        elif data.profession in ['Java_developer', 'Data_analyst']:
            pass

        else:
            data.period = data.period.split('Отсрочка платежа')[-2]

        return data

    def __call__(self, *args, **kwargs):
        """This method serves to use the class instance as a function"""
        return self._parse_data(*args, **kwargs)
