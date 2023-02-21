from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import gather, create_task
# ------------------------------------------------------------------------


async def parse_url(parse_data: dict, session: ClientSession, parser):
    url = parse_data.get('url')

    async with session.get(url) as response:
        result = await response.text()
        sup = BeautifulSoup(result, 'html.parser')
        parsed_data = parser(parse_data, sup)

        return parsed_data


async def event_loop(parse_task: list, parser):
    tasks = []
    async with ClientSession() as session:
        for school in parse_task:
            task = create_task(parse_url(school, session, parser))
            tasks.append(task)

        task_dict = await gather(*tasks)

    return task_dict
