import abc
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt

from passlib.context import CryptContext

from .models.token import TokenData
from .models.user import UserWithPassword

from authentication.repositories.user import get_user_repository, UserRepository


class AuthenticationService(abc.ABC):
    def verify_password(self, plain_password, hashed_password):
        pass

    def get_password_hash(self, password):
        pass

    async def authenticate_user(self, login: str, password: str):
        pass

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        pass

    async def get_current_user(self, token: str):
        pass

    async def sign_up_user(self, user: UserWithPassword):
        pass


class AuthenticationServiceImpl(AuthenticationService):
    __SECRET_KEY = "3d295084712ada79ef7c74ffa465422f769184a50114c066574acfe1bb392e5e"

    __ALGORITHM = "HS256"

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    async def authenticate_user(self, login: str, password: str):
        user = await self.__user_repository.get_by_login(login)
        user = UserWithPassword(**user)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

        return encoded_jwt

    async def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM])
            login: str = payload.get("sub")
            if login is None:
                raise credentials_exception
            token_data = TokenData(login=login)
        except JWTError:
            raise credentials_exception
        user = await self.__user_repository.get_by_login(login=token_data.login)
        if user is None:
            raise credentials_exception
        return user

    async def sign_up_user(self, user: UserWithPassword):
        user = user.copy()
        user.password = self.get_password_hash(user.password)
        return await self.__user_repository.create(user)


def get_authentication_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthenticationService:
    return AuthenticationServiceImpl(user_repository)
