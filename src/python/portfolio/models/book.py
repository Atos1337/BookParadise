from pydantic import BaseModel
from typing import Optional


class PortfolioBookIn(BaseModel):
    book_id: int
    rating: Optional[int]


class PortfolioBook(PortfolioBookIn):
    user_id: int


class PortfolioBookOut(PortfolioBook):
    pass


class Book(BaseModel):
    id: int
    title: str
    author: str
    pages: int
