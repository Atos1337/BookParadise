import datetime

from pydantic import BaseModel


class QuoteCommentBase(BaseModel):
    quote_id: int
    content: str


class QuoteCommentIn(QuoteCommentBase):
    pass


class QuoteComment(QuoteCommentBase):
    user_id: int


class QuoteCommentOut(QuoteComment):
    posted_at: datetime.datetime
