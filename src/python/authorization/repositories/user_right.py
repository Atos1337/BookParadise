import abc

import databases

from fastapi import Depends
from authorization.models.user_right import UserRight
from authorization.database import UserRightInDb
from database import get_db


class UserRightRepository(abc.ABC):
    async def add_right(self, right: UserRight):
        pass

    async def remove_right(self, right: UserRight):
        pass

    async def get_right(self, right: UserRight):
        pass


class UserRightRepositoryImpl(UserRightRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def add_right(self, right: UserRight):
        query = UserRightInDb.insert().values(**right.dict())

        return await self.__db.execute(query=query)

    async def remove_right(self, right: UserRight):
        query = UserRightInDb.delete().where(UserRightInDb.c.user_to == right.user_to and
                                             UserRightInDb.c.user_from == right.user_from and
                                             UserRightInDb.c.kind == right.kind)

        return await self.__db.execute(query=query)

    async def get_right(self, right: UserRight):
        query = UserRightInDb.select().where(UserRightInDb.c.user_to == right.user_to and
                                             UserRightInDb.c.user_from == right.user_from and
                                             UserRightInDb.c.kind == right.kind)

        return await self.__db.fetch_one(query=query)


def get_user_right_repository(db: databases.Database = Depends(get_db)):
    return UserRightRepositoryImpl(db)
