"""This unit contains functions for asynchronous processing"""
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import gather, create_task
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


async def parse_url(parse_data: dict,
                    session: ClientSession,
                    parser: BaseParser.parse_data) -> dict:
    """This async function serves to parse a single URL
    :param parse_data: a dictionary with necessary parsing information such
    as url, tags, etc.
    :param session: a ClientSession's instance of aiohttp package
    :param parser: a parse_data method of BaseParser instance for
    asynchronous parsing
    :return: a dictionary filled with data parsing from the URL
    """
    url = parse_data.get('url')

    async with session.get(url) as response:
        result = await response.text()
        sup = BeautifulSoup(result, 'html.parser')
        parsed_data = parser(parse_data, sup)

        return parsed_data


async def event_loop(parse_task: list,
                     parser: BaseParser.parse_data) -> tuple:
    """This function is an event loop for asynchronous parsing
    :param parse_task: a list of dictionaries with necessary parsing
    information
    :param parser: a parse_data method of BaseParser instance for asynchronous
    parsing
    :return: a tuple containing the parsed data
    """
    tasks = []
    async with ClientSession() as session:
        for school in parse_task:
            task = create_task(parse_url(school, session, parser))
            tasks.append(task)

        finished_tasks = await gather(*tasks)

    return finished_tasks
