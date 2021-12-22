from .service import get_authentication_service, AuthenticationService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .models.user import UserWithId

ACCESS_TOKEN_EXPIRE_MINUTES = 90

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/sign-in")


async def get_current_user(authentication_service: AuthenticationService = Depends(get_authentication_service),
                           token: str = Depends(oauth2_scheme)) -> UserWithId:
    return UserWithId(**await authentication_service.get_current_user(token))
