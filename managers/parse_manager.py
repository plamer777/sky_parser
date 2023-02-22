from asyncio import run
from async_utils import event_loop
from utils import init_sync_driver
from concurrent.futures import ThreadPoolExecutor, as_completed
# ------------------------------------------------------------------------


class ParseManager:
    def __init__(self, parsers: dict, parse_mapper: dict):
        self.parsers = parsers
        self.parser_mapper = parse_mapper
        self.parser_type = {'async': self._async_parser,
                            'sync': self._sync_parser}

    def parse_all(self, parse_data: dict):

        for key in parse_data:
            parser_type = self.parser_mapper.get(key)
            if not parser_type:
                print('Cannot find parser type for the data')
                return parse_data

            result = self.parser_type[parser_type](parse_data[key],
                                                   self.parsers[key])
            parse_data[key] = result

        return parse_data

    @staticmethod
    def _async_parser(data, async_parser):

        try:
            result = run(event_loop(data, async_parser))
            return result
        except Exception as e:
            print(f'There is an error during async parsing: {e}')
            return data

    @staticmethod
    def _sync_parser(data, sync_parser):
        result = []

        for attempt in range(20):
            with ThreadPoolExecutor() as executor:
                tasks = []

                for task in data:
                    if task['price']:
                        continue
                    print(f'{task["url"]} in process')
                    driver = init_sync_driver()
                    tasks.append(executor.submit(sync_parser, task, driver))

                for finished_task in as_completed(tasks):
                    parsed_data = finished_task.result()
                    if parsed_data['price']:
                        print('task finished')
                        result.append(parsed_data)
                    else:
                        print(f'{parsed_data["url"]} failed, one more attempt')
            if len(result) == len(data):
                break
        else:
            print(f'There is an error during sync parsing, 20 attempts are '
                  f'run out')
        return result
