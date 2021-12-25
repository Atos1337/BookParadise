import datetime

from pydantic import BaseModel
from typing import Optional


class QuoteIn(BaseModel):
    content: str
    book_id: Optional[int]


class RepliedQuote(BaseModel):
    replied_quote_id: int


class RepliedQuoteIn(RepliedQuote):
    replied_user_id: int  # чью цитату реплаим для удобства


class Quote(BaseModel):
    user_id: int
    replied_quote_id: Optional[int]
    book_id: Optional[int]
    content: Optional[str]


class QuoteOut(Quote):
    id: int
    posted_at: datetime.datetime
