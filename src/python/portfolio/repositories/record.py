import abc

import databases

from fastapi import Depends
from database import get_db
from portfolio.models.record import PortfolioRecord, PortfolioStatistics
from portfolio.database import PortfolioRecordInDb
from sqlalchemy import select, func, column


class PortfolioRecordRepository(abc.ABC):
    async def add_record(self, record: PortfolioRecord):
        pass

    async def get_records(self, user_id: int):
        pass

    async def get_portfolio_statistics(self, user_id: int):
        pass


class PortfolioRecordRepositoryImpl(PortfolioRecordRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def add_record(self, record: PortfolioRecord):
        query = PortfolioRecordInDb.insert().values(**record.dict())

        return await self.__db.execute(query=query)

    async def get_records(self, user_id: int):
        query = PortfolioRecordInDb.select().where(PortfolioRecordInDb.c.user_id == user_id)

        return await self.__db.fetch_all(query=query)

    async def get_portfolio_statistics(self, user_id: int):
        query = select([column(key) for key in PortfolioStatistics.__fields__.keys()])\
            .select_from(func.book_paradise.get_portfolio_statistics(user_id))

        return await self.__db.fetch_one(query=query)


def get_portfolio_record_repository(db: databases.Database = Depends(get_db)):
    return PortfolioRecordRepositoryImpl(db)
