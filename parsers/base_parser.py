"""This file contains a BaseParser class to be inherited by all parsers"""
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from parse_classes.school_parse_task import ProfessionParseRequest
# ------------------------------------------------------------------------


class BaseParser(ABC):
    """This abstract class provides an interface for all parsers"""
    @abstractmethod
    def _parse_data(self, parse_data: ProfessionParseRequest,
                   driver: BeautifulSoup | WebDriver):
        """The main method to parse data"""
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """This method serves to use parser as a function"""
        pass
