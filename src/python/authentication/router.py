from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from .models.token import Token
from .models.user import User, UserIn, UserOut, UserInDB
from .api import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, \
    get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from src.python.database.repositories.user import UserRepository, get_user_repository
from src.python.database.api import db

auth = APIRouter()


@auth.on_event("startup")
async def startup():
    await db.connect()


@auth.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 user_repository: UserRepository = Depends(get_user_repository)):
    user = await authenticate_user(user_repository, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth.post("/sign-up", response_model=UserOut)
async def sing_up_new_user(user: UserIn, user_repository: UserRepository = Depends(get_user_repository)):
    user_with_hashed_password = UserInDB(login=user.login, hashed_password=user.password)
    user_with_hashed_password.hashed_password = get_password_hash(user_with_hashed_password.hashed_password)
    user_id = await user_repository.create(user_with_hashed_password)

    return {**user.dict(), "id": user_id}
