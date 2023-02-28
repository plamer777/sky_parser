"""This file contains LoggingManager class to create loggers by provided
settings"""
import logging
from error_classes.logging_errors import FileHandlerError, FormatterError
# ------------------------------------------------------------------------


class LoggingManager:
    """LoggingManager class provides simple way to create loggers"""
    def __init__(self, log_file_path: str, format_str: str) -> None:
        """Initialization of LoggingManager class
        :param log_file_path: path to the log file
        :param format_str: special format string to generate log messages
        """
        self._log_filename = log_file_path
        self._format_str = format_str
        self._file_handler = self._set_file_handler()
        self._formatter = self._set_log_format()

    def _set_file_handler(self) -> logging.FileHandler:
        """The method serves to create a file handler
        :return: a configured file handler
        """
        file_handler = logging.FileHandler(
            self._log_filename, encoding='utf-8')
        return file_handler

    def _set_log_format(self) -> logging.Formatter:
        """The method serves to create a formatter object
        :return: a configured formatter object
        """
        formatter = logging.Formatter(self._format_str)
        return formatter

    def get_logger(self, name: str, level: int):
        """This is a main method to get a new logger
        :param name: name of the logger
        :param level: level of the logger (DEBUG, INFO, WARNING, ERROR, etc)
        :return: a configured logger object
        """
        if self._file_handler is None:
            raise FileHandlerError('Filehandler was not initialized')
        elif self._formatter is None:
            raise FormatterError('Formatter was not initialized')

        logger = logging.getLogger(name)
        logger.setLevel(level)

        self._file_handler.setFormatter(self._formatter)
        logger.addHandler(self._file_handler)

        return logger


