import abc
import databases

from fastapi import Depends
from database import get_db
from quotes.models.quote import Quote, QuoteOut
from quotes.database import QuoteInDb


class QuoteRepository(abc.ABC):
    async def add(self, quote: Quote):
        pass

    async def add_book_to_quote(self, user_id: int, quote_id: int, book_id: int):
        pass

    async def get_by_user_id(self, user_id: int):
        pass

    async def get_by_id(self, quote_id: int):
        pass


class QuoteRepositoryImpl(QuoteRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def add(self, quote: Quote):
        query = QuoteInDb.insert().values(**quote.dict())

        return await self.__db.execute(query=query)

    async def add_book_to_quote(self, user_id: int, quote_id: int, book_id: int):
        query = QuoteInDb.update().where(
            QuoteInDb.c.id == quote_id and QuoteInDb.c.user_id == user_id
        ).values(book_id=book_id)

        return await self.__db.execute(query=query)

    async def get_by_user_id(self, user_id: int):
        query = QuoteInDb.select().where(QuoteInDb.c.user_id == user_id)

        return await self.__db.fetch_all(query=query)

    async def get_by_id(self, quote_id: int):
        query = QuoteInDb.select().where(QuoteInDb.c.id == quote_id)

        return QuoteOut(**await self.__db.fetch_one(query=query))


def get_quote_repository(db: databases.Database = Depends(get_db)):
    return QuoteRepositoryImpl(db)
