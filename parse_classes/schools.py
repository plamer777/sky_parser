from typing import Union
from pydantic import BaseModel
# ----------------------------------------------------------------------------


class ProfessionParseRequest(BaseModel):
    profession: str = None
    pro_price_tags: list[str] = None
    middle_price_tags: list[str] = None
    additional_price_tags: list[str] = None
    price_tags: list[str] = None
    period_tags: Union[list[str], str] = None
    total_tags: list[str] = None
    url: str = None


class ProfessionParseResponse(BaseModel):
    profession: str = None
    price: Union[int, str] = ''
    period: Union[float, int, str] = ''
    total: Union[int, str] = ''
    middle_price: Union[int, str] = None
    pro_price: Union[int, str] = None
    course_level: str = None


class SchoolParseTask(BaseModel):
    school_name: str = None
    parse_requests: list[ProfessionParseRequest] = []
    parse_responses: list[ProfessionParseResponse] = []
