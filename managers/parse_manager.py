from asyncio import run
from async_utils import event_loop
from utils import init_sync_driver


class ParseManager:
    def __init__(self, parsers: dict, parse_mapper: dict):
        self.parsers = parsers
        self.parser_mapper = parse_mapper
        self.parser_type = {'async': self._async_parser,
                            'sync': self._sync_parser}

    def parse_all(self, parse_data: dict):
        for key in parse_data:
            parser_type = self.parser_mapper[key]

            result = self.parser_type[parser_type](parse_data[key],
                                                        self.parsers[key])

            parse_data[key] = result

        return parse_data

    @staticmethod
    def _async_parser(data, async_parser):

        result = run(event_loop(data, async_parser))
        return result

    @staticmethod
    def _sync_parser(data, sync_parser):
        driver = init_sync_driver()

        result = []
        for task in data:
            print(f'{task} in process')
            task = sync_parser(task, driver)
            result.append(task)

        driver.close()
        return result
