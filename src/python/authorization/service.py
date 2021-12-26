import abc

from fastapi import Depends

from .models.user_right import UserRight
from .repositories.user_right import UserRightRepository, get_user_right_repository


class AuthorizationService(abc.ABC):
    async def add_right(self, right: UserRight):
        pass

    async def remove_right(self, right: UserRight):
        pass

    async def is_exist(self, right: UserRight):
        pass


class AuthorizationServiceImpl(AuthorizationService):
    def __init__(self, user_right_repository: UserRightRepository):
        self.__user_right_repository = user_right_repository

    async def add_right(self, right: UserRight):
        return await self.__user_right_repository.add_right(right)

    async def remove_right(self, right: UserRight):
        return await self.__user_right_repository.remove_right(right)

    async def is_exist(self, right: UserRight):
        if right.user_to == right.user_from:
            return True

        existed_right = await self.__user_right_repository.get_right(right)

        if existed_right is None:
            return False

        return True


def get_authorization_service(user_right_repository: UserRightRepository = Depends(get_user_right_repository)):
    return AuthorizationServiceImpl(user_right_repository)
