"""This unit contains an error classes for ParseManager class"""


class FileHandlerError(Exception):
    """This exception raises if FileHandler wasn't provided"""
    pass


class FormatterError(Exception):
    """This exception raises if Formatter wasn't provided"""
    pass
