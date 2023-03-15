"""This unit contains functions for asynchronous processing"""
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import gather, create_task
from parse_classes.school_parse_task import ProfessionParseRequest
from parsers.base_parser import BaseParser
# ------------------------------------------------------------------------


async def parse_url(parse_request: ProfessionParseRequest,
                    session: ClientSession,
                    parser: BaseParser):
    """This async function serves to parse a single URL
    :param parse_request: a ProfessionParseRequest instance with necessary
    parsing information such as url, tags, etc.
    :param session: a ClientSession's instance of aiohttp package
    :param parser: an instance of class inherited from BaseParser for
    asynchronous parsing
    :return: a dictionary filled with data parsing from the URL
    """
    url = getattr(parse_request, 'url', None)

    async with session.get(url) as response:
        result = await response.text()
        sup = BeautifulSoup(result, 'html.parser')
        parse_response = parser(parse_request, sup)

        return parse_response


async def event_loop(
        parse_tasks: list[ProfessionParseRequest],
        parser: BaseParser):
    """This function is an event loop for asynchronous parsing
    :param parse_tasks: a list of ProfessionParseRequest instances with
    necessary parsing information
    :param parser: an instance of class inherited from BaseParser for
    asynchronous parsing
    :return: a Coroutine
    """
    tasks = []
    async with ClientSession() as session:
        for school in parse_tasks:
            task = create_task(parse_url(school, session, parser))
            tasks.append(task)

        finished_tasks = await gather(*tasks)

    return finished_tasks
