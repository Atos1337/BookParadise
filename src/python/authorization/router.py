from fastapi import APIRouter, Depends
from database import db
from .models.user_right import UserRight, UserRightIn
from authentication import get_current_user
from authentication.models.user import UserWithId
from .service import get_authorization_service, AuthorizationService

auth = APIRouter()


@auth.on_event("startup")
async def startup():
    await db.connect()


@auth.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@auth.post("/add", response_model=UserRight)
async def add_right(right: UserRightIn, user: UserWithId = Depends(get_current_user),
                    authorization_service: AuthorizationService = Depends(get_authorization_service)):
    user_right = UserRight(**right.dict(), user_from=user.id)
    await authorization_service.add_right(user_right)
    return user_right


@auth.delete("/remove", response_model=UserRight)
async def remove_right(right: UserRightIn, user: UserWithId = Depends(get_current_user),
                       authorization_service: AuthorizationService = Depends(get_authorization_service)):
    user_right = UserRight(**right.dict(), user_from=user.id)
    await authorization_service.remove_right(user_right)
    return user_right
