from enum import Enum
from pydantic import BaseModel


class RightKindEnum(str, Enum):
    see_quotes = 'see quotes'
    comment_quotes = 'comment quotes'
    see_portfolio = 'see portfolio'


class UserRightIn(BaseModel):
    user_to: int
    kind: RightKindEnum


class UserRight(UserRightIn):
    user_from: int
