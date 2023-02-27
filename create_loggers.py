"""This unit contains an instance of LoggingManager to create loggers"""
import logging
from constants import LOG_PATH, LOG_FORMAT_STR
from managers.logging_manager import LoggingManager
# ------------------------------------------------------------------------

logging_manager = LoggingManager(LOG_PATH, LOG_FORMAT_STR)
logger = logging_manager.get_logger('parse_logger', logging.INFO)
