from asyncio import run
from typing import Any
from async_utils import event_loop
from parsers.base_parser import BaseParser
from utils import init_sync_driver, refactor_data
from concurrent.futures import ThreadPoolExecutor, as_completed
from create_loggers import logger
# ------------------------------------------------------------------------


class ParseManager:
    """ParseManager class serves to manage asynchronous and synchronous
    parsing using provided parsers"""
    def __init__(self, parsers: dict[str, Any], parse_mapper: dict[str,
                 str]) -> None:
        """Initialization of ParseManager class
        :param parsers: Dictionary of parsers
        :param parse_mapper: Dictionary of site names with parse regimes -
        async or sync
        """
        self.parsers = parsers
        self.parser_mapper = parse_mapper
        self.parser_type = {'async': self._async_parser,
                            'sync': self._sync_parser}

    def parse_all(self, parse_data: dict):
        """This is a main method to start parsing by using provided parse
        data with sites, urls and tags
        :param parse_data: Dictionary where keys are site names and values
        are lists of dictionaries with full parse data
        :return: Refactored dictionary with necessary information parsed from
        provided sites
        """
        for key in parse_data:
            parser_type = self.parser_mapper.get(key)

            if not parser_type:
                logger.error(
                    'ParseManager cannot find parser type for the data')
                return parse_data

            result = self.parser_type[parser_type](parse_data[key],
                                                   self.parsers[key])
            parse_data[key] = refactor_data(result)

        return parse_data

    @staticmethod
    def _async_parser(data: list[dict],
                      async_parser: BaseParser) -> list[dict]:
        """This method serves as main asynchronous parser
        :param data: list of dictionaries with full parse data
        :param async_parser: an instance of BaseParser for asynchronous parsing
        :return: a list of dictionaries filled with data received from
        provided sites or initial list instead
        """
        try:
            result = run(event_loop(data, async_parser))
            return result
        except Exception as e:
            logger.error(f'There is an error during async parsing: {e}')
            return data

    @staticmethod
    def _sync_parser(data: list[dict], sync_parser: BaseParser) -> list[dict]:
        """This method serves as main synchronous parser
        :param data: list of dictionaries with full parse data
        :param sync_parser: an instance of BaseParser for synchronous parsing
        :return: a list of dictionaries filled with data received from
        provided sites or initial list otherwise
        """
        result = []

        for attempt in range(20):
            with ThreadPoolExecutor() as executor:
                tasks = []

                for task in data:
                    if task['price']:
                        continue
                    logger.info(f'{task["url"]} in process')
                    driver = init_sync_driver()
                    tasks.append(executor.submit(sync_parser, task, driver))

                for finished_task in as_completed(tasks):
                    parsed_data = finished_task.result()
                    if parsed_data['price']:
                        logger.info(f'Task {parsed_data.get("url")} finished')
                        result.append(parsed_data)
                    else:
                        logger.warning(
                            f'{parsed_data["url"]} failed, one more attempt')

            if len(result) == len(data):
                break
        else:
            logger.exception(
                f'Error during sync parsing, 20 attempts are run out')
            return data

        return result
