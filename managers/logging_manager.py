import logging
from error_classes.logging_errors import FileHandlerError, FormatterError


class LoggingManager:

    def __init__(self, log_file_path: str, format_str: str) -> None:
        self._log_filename = log_file_path
        self._format_str = format_str
        self._file_handler = self._set_file_handler()
        self._formatter = self._set_log_format()

    def _set_file_handler(self) -> logging.FileHandler:
        file_handler = logging.FileHandler(self._log_filename, encoding='utf-8')
        return file_handler

    def _set_log_format(self) -> logging.Formatter:
        formatter = logging.Formatter(self._format_str)
        return formatter

    def get_logger(self, name: str, level: int):
        if self._file_handler is None:
            raise FileHandlerError('Filehandler was not initialized')
        elif self._formatter is None:
            raise FormatterError('Formatter was not initialized')

        logger = logging.getLogger(name)
        logger.setLevel(level)

        self._file_handler.setFormatter(self._formatter)
        logger.addHandler(self._file_handler)

        return logger


