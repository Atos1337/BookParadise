import abc

from fastapi import Depends, HTTPException, status
from .repositories.quote_comment import QuoteCommentRepository, get_quote_comment_repository
from .repositories.quote import QuoteRepository, get_quote_repository
from authentication.models.user import UserWithId
from .models.quote_comment import QuoteCommentBase, QuoteComment
from .models.quote import QuoteOut, QuoteIn, Quote, RepliedQuoteIn
from authorization.service import AuthorizationService, get_authorization_service
from authorization.models.user_right import UserRight


class QuoteService(abc.ABC):
    async def add_quote_comment(self, user: UserWithId, quote_comment: QuoteCommentBase):
        pass

    async def get_quote_comments_by_quote(self, quote_id: int):
        pass

    async def add_quote(self, user: UserWithId, quote: QuoteIn):
        pass

    async def add_replied_quote(self, user: UserWithId, replied_quote: RepliedQuoteIn):
        pass

    async def get_quotes_by_user_id(self, user: UserWithId, user_id: int = None):
        pass

    async def link_book(self, user: UserWithId, quote_id: int, book_id: int):
        pass


class QuoteServiceImpl(QuoteService):
    def __init__(self, authorization_service: AuthorizationService,
                 quote_comment_repository: QuoteCommentRepository,
                 quote_repository: QuoteRepository):
        self.__authorization_service = authorization_service
        self.__quote_comment_repository = quote_comment_repository
        self.__quote_repository = quote_repository

    async def add_quote_comment(self, user: UserWithId, quote_comment: QuoteCommentBase):
        quote: QuoteOut = await self.__quote_repository.get_by_id(quote_comment.quote_id)

        if not await self.__authorization_service.is_exist(UserRight(
                user_from=quote.user_id, user_to=user.id, kind='comment quotes')
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You couldn\'t comment quotes of this user'
            )

        return await self.__quote_comment_repository.add(QuoteComment(**quote_comment.dict(), user_id=user.id))

    # без авторизации, потому что для тестирования
    async def get_quote_comments_by_quote(self, quote_id: int):
        return await self.__quote_comment_repository.get_by_quote(quote_id)

    async def add_quote(self, user: UserWithId, quote: QuoteIn):
        return await self.__quote_repository.add(Quote(**quote.dict(), user_id=user.id))

    async def add_replied_quote(self, user: UserWithId, replied_quote: RepliedQuoteIn):
        await self.__check_can_see_quotes(user, replied_quote.replied_user_id)

        return await self.__quote_repository.add(Quote(**replied_quote.dict(), user_id=user.id))

    async def get_quotes_by_user_id(self, user: UserWithId, user_id: int = None):
        if not user_id:
            user_id = user.id
        else:
            await self.__check_can_see_quotes(user, user_id)

        return await self.__quote_repository.get_by_user_id(user_id)

    async def link_book(self, user: UserWithId, quote_id: int, book_id: int):
        return await self.__quote_repository.add_book_to_quote(user.id, quote_id, book_id)

    async def __check_can_see_quotes(self, user: UserWithId, user_id):
        if not await self.__authorization_service.is_exist(UserRight(
            user_from=user_id, user_to=user.id, kind='see quotes'
        )):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You couldn\'t see quotes of this user'
            )


def get_quote_service(authorization_service: AuthorizationService = Depends(get_authorization_service),
                      quote_comment_repository: QuoteCommentRepository = Depends(get_quote_comment_repository),
                      quote_repository: QuoteRepository = Depends(get_quote_repository)):
    return QuoteServiceImpl(authorization_service, quote_comment_repository, quote_repository)
