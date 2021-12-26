from fastapi import APIRouter, Depends
from database import db
from .models.book import PortfolioBookOut, Book, PortfolioBookIn
from .models.record import PortfolioStatistics, PortfolioRecordOut, PortfolioRecordIn
from .service import PortfolioService, get_portfolio_service
from authentication import get_current_user, UserWithId
from typing import List


port = APIRouter()


@port.on_event("startup")
async def startup():
    await db.connect()


@port.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@port.post("/book")
async def add_book(book: PortfolioBookIn, user: UserWithId = Depends(get_current_user),
                   portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.add_book(user, book)


@port.get("/book", response_model=List[PortfolioBookOut])
async def get_books(user_id: int = None, user: UserWithId = Depends(get_current_user),
                    portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.get_books(user, user_id)


@port.put("/book/rate")
async def rate_book(book_id: int, rating: int, user: UserWithId = Depends(get_current_user),
                    portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.rate_book(user, book_id, rating)


@port.get("/intersection", response_model=List[Book])
async def get_portfolio_intersection(user_id: int, user: UserWithId = Depends(get_current_user),
                                     portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.get_portfolio_intersection(user, user_id)


@port.get("/statistics", response_model=PortfolioStatistics)
async def get_portfolio_statistics(user_id: int, user: UserWithId = Depends(get_current_user),
                                   portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.get_portfolio_statistics(user, user_id)


@port.post("/record")
async def add_record(record: PortfolioRecordIn, user: UserWithId = Depends(get_current_user),
                     portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.add_record(user, record)


@port.get("/record", response_model=List[PortfolioRecordOut])
async def get_records(user_id: int = None, user: UserWithId = Depends(get_current_user),
                      portfolio_service: PortfolioService = Depends(get_portfolio_service)):
    return await portfolio_service.get_records(user, user_id)
