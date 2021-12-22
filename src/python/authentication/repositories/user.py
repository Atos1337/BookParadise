import abc

import databases

from fastapi import Depends
from src.python.authentication.models.user import UserWithPassword
from src.python.database import get_db
from src.python.authentication.database import UserInfoInDb


class UserRepository(abc.ABC):
    async def get_by_login(self, login: str):
        pass

    async def create(self, user: UserWithPassword):
        pass


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: databases.Database):
        self.__db = db

    async def get_by_login(self, login: str):
        query = UserInfoInDb.select(UserInfoInDb.c.login == login)

        return await self.__db.fetch_one(query=query)

    async def create(self, user: UserWithPassword):
        query = UserInfoInDb.insert().values(**user.dict())

        return await self.__db.execute(query=query)


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)
