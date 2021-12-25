from fastapi import APIRouter, Depends
from .models.quote_comment import QuoteCommentOut, QuoteCommentIn
from .models.quote import QuoteOut, QuoteIn, RepliedQuoteIn
from authentication import get_current_user, UserWithId
from .service import get_quote_service, QuoteService
from typing import List


quotes = APIRouter()


@quotes.post("/quote-comment/add", response_model=int)
async def add_quote_comment(quote_comment: QuoteCommentIn,
                            user: UserWithId = Depends(get_current_user),
                            quotes_service: QuoteService = Depends(get_quote_service)):
    return await quotes_service.add_quote_comment(user, quote_comment)


@quotes.get("/quote-comment/", response_model=List[QuoteCommentOut])
async def get_quote_comment_by_quote_id(quote_id: int, quotes_service: QuoteService = Depends(get_quote_service)):
    return await quotes_service.get_quote_comments_by_quote(quote_id)


@quotes.post("/add", response_model=int)
async def add_quote(quote: QuoteIn,
                    user: UserWithId = Depends(get_current_user),
                    quotes_service: QuoteService = Depends(get_quote_service)):
    return await quotes_service.add_quote(user, quote)


@quotes.post("/reply", response_model=int)
async def reply_quote(quote: RepliedQuoteIn,
                      user: UserWithId = Depends(get_current_user),
                      quotes_service: QuoteService = Depends(get_quote_service)):
    return await quotes_service.add_replied_quote(user, quote)


@quotes.get("/", response_model=List[QuoteOut])
async def get_quotes_by_user_id(user_id: int = None,
                                user: UserWithId = Depends(get_current_user),
                                quotes_service: QuoteService = Depends(get_quote_service)):
    return await quotes_service.get_quotes_by_user_id(user, user_id)


@quotes.put("/link/")
async def link_book(quote_id: int, book_id: int,
                    user: UserWithId = Depends(get_current_user),
                    quotes_service: QuoteService = Depends(get_quote_service)):
    await quotes_service.link_book(user, quote_id, book_id)
    return {"status": "OK"}
