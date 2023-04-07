"""This file contains classes representing the parse responses and requests"""
from typing import Union
from pydantic import BaseModel
# ----------------------------------------------------------------------------


class BaseProfessionParseTask(BaseModel):
    """The base class containing common fields"""
    profession: str = None
    url: str = None
    middle_price: Union[int, str, None] = None
    pro_price: Union[int, str, None] = None


class ProfessionParseRequest(BaseProfessionParseTask):
    """The ProfessionParseRequest class represents a request to parse"""
    pro_price_tags: list[str] = None
    middle_price_tags: list[str] = None
    additional_price_tags: list[str] = None
    price_tags: list[str] = None
    period_tags: Union[list[str], str] = None
    total_tags: list[str] = None

    class Config:
        orm_mode = True


class ProfessionParseResponse(BaseProfessionParseTask):
    """This class represents a response with results of the parsing"""
    price: Union[int, str, float, None] = ''
    period: Union[float, int, str, None] = ''
    middle_period: Union[float, int, str] = None
    pro_period: Union[float, int, str] = None
    price_change: int = 0
    period_change: int = 0
    total: Union[int, str, float, None] = ''
    course_level: str = None
    updated_at: str = None

    class Config:
        orm_mode = True


class SchoolParseTask(BaseModel):
    """The SchoolParseTask class represents a parsing task containing
    requests and responses"""
    school_name: str = None
    parse_requests: list[ProfessionParseRequest] = []
    parse_responses: list[ProfessionParseResponse] = []
