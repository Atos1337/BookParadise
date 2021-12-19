import abc

import databases

from src.python.authentication.models.user import UserInDB
from src.python.database.api import get_db, UserInfoInDb


class UserRepository(abc.ABC):
    async def get_by_login(self, login: str):
        pass

    async def create(self, user: UserInDB):
        pass


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: databases.Database = get_db()):
        self.db = db

    async def get_by_login(self, login: str):
        query = UserInfoInDb.select(UserInfoInDb.c.login == login)

        return await self.db.fetch_one(query=query)

    async def create(self, user: UserInDB):
        query = UserInfoInDb.insert().values(**user.dict())

        return await self.db.execute(query=query)


user_repository = UserRepositoryImpl()


def get_user_repository() -> UserRepository:
    return user_repository
