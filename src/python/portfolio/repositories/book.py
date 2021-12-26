import abc

import databases

from fastapi import Depends
from database import get_db
from portfolio.models.book import PortfolioBook, Book
from portfolio.database import PortfolioBookInDb
from sqlalchemy import select, func, column


class PortfolioBookRepository(abc.ABC):
    async def add_book(self, book: PortfolioBook):
        pass

    async def rate_book(self, book_id: int, user_id: int, rating: int):
        pass

    async def get_books(self, user_id: int):
        pass

    async def get_portfolio_intersection(self, user_id1: int, user_id2: int):
        pass


class PortfolioBookRepositoryImpl(PortfolioBookRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def add_book(self, book: PortfolioBook):
        query = PortfolioBookInDb.insert().values(**book.dict())

        return await self.__db.execute(query=query)

    async def rate_book(self, book_id: int, user_id: int, rating: int):
        query = PortfolioBookInDb.update().where(PortfolioBookInDb.c.book_id == book_id and
                                                 PortfolioBookInDb.c.user_id == user_id).values(rating=rating)

        return await self.__db.execute(query=query)

    async def get_books(self, user_id: int):
        query = PortfolioBookInDb.select().where(PortfolioBookInDb.c.user_id == user_id)

        return await self.__db.fetch_all(query=query)

    async def get_portfolio_intersection(self, user_id1: int, user_id2: int):
        query = select([column(key) for key in Book.__fields__.keys()])\
            .select_from(func.book_paradise.get_portfolio_intersection(user_id1, user_id2))

        return await self.__db.fetch_all(query=query)


def get_portfolio_book_repository(db: databases.Database = Depends(get_db)):
    return PortfolioBookRepositoryImpl(db)
