import abc

from fastapi import Depends, HTTPException, status
from .repositories.record import PortfolioRecordRepository, get_portfolio_record_repository
from .repositories.book import PortfolioBookRepository, get_portfolio_book_repository
from authentication.models.user import UserWithId
from .models.record import PortfolioRecordIn, PortfolioRecord
from authorization.service import AuthorizationService, get_authorization_service
from .models.book import PortfolioBook, PortfolioBookIn
from authorization.models.user_right import UserRight


class PortfolioService(abc.ABC):
    async def add_book(self, user: UserWithId, book: PortfolioBookIn):
        pass

    async def rate_book(self, user: UserWithId, book_id: int, rating: int):
        pass

    async def get_books(self, user: UserWithId, user_id: int):
        pass

    async def get_portfolio_intersection(self, user: UserWithId, user_id: int):
        pass

    async def add_record(self, user: UserWithId, record: PortfolioRecordIn):
        pass

    async def get_records(self, user: UserWithId, user_id: int):
        pass

    async def get_portfolio_statistics(self, user: UserWithId, user_id: int):
        pass


class PortfolioServiceImpl(PortfolioService):
    def __init__(self, portfolio_record_repository: PortfolioRecordRepository,
                 portfolio_book_repository: PortfolioBookRepository,
                 authorization_service: AuthorizationService):
        self.__portfolio_record_repository = portfolio_record_repository
        self.__portfolio_book_repository = portfolio_book_repository
        self.__authorization_service = authorization_service

    async def add_book(self, user: UserWithId, book: PortfolioBookIn):
        return await self.__portfolio_book_repository.add_book(PortfolioBook(**book.dict(), user_id=user.id))

    async def rate_book(self, user: UserWithId, book_id: int, rating: int):
        return await self.__portfolio_book_repository.rate_book(book_id, user.id, rating)

    async def get_books(self, user: UserWithId, user_id: int):
        if user_id is not None:
            await self.__check_can_see_portfolio(user, user_id)

        return await self.__portfolio_book_repository.get_books(user_id)

    async def get_portfolio_intersection(self, user: UserWithId, user_id: int):
        if user_id != user.id:
            await self.__check_can_see_portfolio(user, user_id)

        return await self.__portfolio_book_repository.get_portfolio_intersection(user.id, user_id)

    async def add_record(self, user: UserWithId, record: PortfolioRecordIn):
        return await self.__portfolio_record_repository.add_record(PortfolioRecord(**record.dict(), user_id=user.id))

    async def get_records(self, user: UserWithId, user_id: int):
        if user_id is not None:
            await self.__check_can_see_portfolio(user, user_id)

        return await self.__portfolio_record_repository.get_records(user_id)

    async def get_portfolio_statistics(self, user: UserWithId, user_id: int):
        if user.id != user_id:
            await self.__check_can_see_portfolio(user, user_id)

        return await self.__portfolio_record_repository.get_portfolio_statistics(user_id)

    async def __check_can_see_portfolio(self, user: UserWithId, user_id: int):
        if not await self.__authorization_service.is_exist(UserRight(
            user_from=user_id, user_to=user.id, kind='see portfolio'
        )):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You can\'t see portfolio of this user'
            )


def get_portfolio_service(
        portfolio_record_repository: PortfolioRecordRepository = Depends(get_portfolio_record_repository),
        portfolio_book_repository: PortfolioBookRepository = Depends(get_portfolio_book_repository),
        authorization_service: AuthorizationService = Depends(get_authorization_service)
):
    return PortfolioServiceImpl(portfolio_record_repository, portfolio_book_repository, authorization_service)
