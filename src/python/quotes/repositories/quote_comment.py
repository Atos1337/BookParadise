import abc

import databases

from fastapi import Depends
from database import get_db
from quotes.models.quote_comment import QuoteComment
from quotes.database import QuoteCommentInDb


class QuoteCommentRepository(abc.ABC):
    async def add(self, quote_comment: QuoteComment):
        pass

    async def get_by_quote(self, quote_id):
        pass


class QuoteCommentRepositoryImpl(QuoteCommentRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def add(self, quote_comment: QuoteComment):
        query = QuoteCommentInDb.insert().values(**quote_comment.dict())

        return await self.__db.execute(query=query)

    async def get_by_quote(self, quote_id):
        query = QuoteCommentInDb.select().where(QuoteCommentInDb.c.quote_id == quote_id)

        return await self.__db.fetch_all(query=query)


def get_quote_comment_repository(db: databases.Database = Depends(get_db)):
    return QuoteCommentRepositoryImpl(db)
