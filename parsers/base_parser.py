from abc import ABC, abstractmethod
# ------------------------------------------------------------------------


class BaseParser(ABC):

    @abstractmethod
    def parse_data(self, parse_data: dict, driver):
        pass
