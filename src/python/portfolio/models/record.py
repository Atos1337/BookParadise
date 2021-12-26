import datetime
from pydantic import BaseModel


class PortfolioRecordIn(BaseModel):
    book_id: int
    pages: int


class PortfolioRecord(PortfolioRecordIn):
    user_id: int


class PortfolioRecordOut(PortfolioRecord):
    posted_at: datetime.datetime


class PortfolioStatistics(BaseModel):
    book_id: int
    read_pages: int
    remain_pages: int
    wasted_time: int
