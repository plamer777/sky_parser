"""This unit contains ParseManager class to rule parsing processes"""
from asyncio import run
from typing import Any, Union, Iterator
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from async_utils import event_loop
from constants import MULTY_THREAD_ATTEMPTS, ASYNC_ATTEMPTS
from parse_classes.school_parse_task import SchoolParseTask, \
    ProfessionParseRequest, ProfessionParseResponse
from parsers.base_parser import BaseParser
from utils import refactor_parse_responses
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
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
        self._parsers = parsers
        self._parser_mapper = parse_mapper
        self._parser_type = {'async': self._async_parser,
                             'sync': self._multi_thread_parser}

    def parse_all(
            self, parse_data: list[SchoolParseTask]) -> list[SchoolParseTask]:
        """This is a main method to start parsing by using provided parse
        data with urls and tags
        :param parse_data: A list of SchoolParseTask instances with having
        parse request class with urls and tags necessary to parse data from
        sites
        :return: A SchoolParseTask instances filled with
        ProfessionParseResponse instances containing data extracted from sites
        """
        for task in parse_data:
            parser_type = self._parser_mapper.get(task.school_name)

            if not parser_type:
                logger.error(
                    'ParseManager cannot find parser type for the data')
                continue

            result = self._parser_type[parser_type](
                task.parse_requests, self._parsers[task.school_name])

            task.parse_responses.extend(refactor_parse_responses(result))

        return parse_data

    def _async_parser(
            self,
            parse_requests: list[ProfessionParseRequest],
            parser: BaseParser) -> list[ProfessionParseResponse]:
        """This method serves as main asynchronous parser
        :param parse_requests: list of ProfessionParseRequest instances with
        parse tags and urls
        :param parser: an instance of BaseParser for asynchronous parsing
        using BeautifulSoup package
        :return: a list of ProfessionParseResponse instances filled with data
        received from sites or a list of empty instances instead
        """
        try:
            total_parsed = []
            for _ in range(ASYNC_ATTEMPTS):
                result = run(event_loop(parse_requests, parser))
                parsed, unparsed = self._sort_parsed_unparsed(result)
                total_parsed.extend(parsed)

                if not unparsed:
                    print('Asynch batch parsed successfully')
                    return total_parsed

                parse_requests = unparsed

            logger.error(f'Failed to parse {unparsed} attempts run out')
            total_parsed.extend([
                ProfessionParseResponse.from_orm(item)
                for item in unparsed
            ])

            return total_parsed

        except Exception as e:
            print(f'There is an error during async parsing: {e}')
            return [
                ProfessionParseResponse().from_orm(item)
                for item in parse_requests
            ]

    def _multi_thread_parser(
            self,
            parse_requests: list[ProfessionParseRequest],
            parser: BaseParser) -> list[ProfessionParseResponse]:
        """This method serves as main multithread parser
        :param parse_requests: list of ProfessionParseRequest instances
        with tags and urls to parse
        :param parser: an instance of BaseParser for multithread
        parsing using selenium package
        :return: a list of ProfessionParseResponse instances filled with data
        received from provided sites or an empty instances otherwise
        """
        result = []
        for attempt in range(MULTY_THREAD_ATTEMPTS):

            with ThreadPoolExecutor() as executor:
                tasks = []
                for task in parse_requests:
                    print(f'{task.url} in process')
                    driver = self._init_sync_driver()
                    tasks.append(executor.submit(parser, task, driver))

                finished = as_completed(tasks)
                parsed, unparsed = self._sort_parsed_unparsed(finished)

                result.extend(parsed)
                if not unparsed:
                    return result

            parse_requests = unparsed

        logger.error(f'Error during sync parsing, 30 attempts are run out')
        result.extend([
                ProfessionParseResponse.from_orm(item)
                for item in unparsed
            ])
        return result

    @staticmethod
    def _sort_parsed_unparsed(
            data: Union[Iterator[Future], list[ProfessionParseResponse],
                        list[ProfessionParseRequest]]) -> tuple[list, list]:
        """This method sorts provided data into parsed and unparsed
        :param data: a list of ProfessionParseResponse, ProfessionParseRequest
        instances or Iterator containing Futures
        :return: a tuple of lists of parsed and unparsed data
        """
        unparsed = []
        parsed = []
        for row in data:
            if type(row) is Future:
                row = row.result()
            if not getattr(row, 'price', None):
                print(f'{row.url} failed, one more attempt')
                unparsed.append(row)
            else:
                print(f'Task {row.url} finished')
                parsed.append(row)

        return parsed, unparsed

    @staticmethod
    def _init_sync_driver() -> WebDriver | None:
        """This method initializes the sync selenium driver to parse sites with
        JS or having another problems for standard asynchronous parsing
        :return: a configured WebDriver instance
        """
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1240x1024")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(
                "--disable-blink-features=AutomationControlled")

            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            logger.error(
                f'There was an error in the init_sync_driver function: {e}')
            return None
