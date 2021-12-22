from datetime import timedelta

import asyncpg.exceptions
from fastapi import APIRouter, Depends, HTTPException, status
from .models.token import Token
from .models.user import UserWithPassword, UserWithId
from .service import get_authentication_service, AuthenticationService
from fastapi.security import OAuth2PasswordRequestForm
from src.python.database import db
from . import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

auth = APIRouter()


@auth.on_event("startup")
async def startup():
    await db.connect()


@auth.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@auth.post("/sign-in", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 authentication_service: AuthenticationService = Depends(get_authentication_service)):
    user = await authentication_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication_service.create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get("/me", response_model=UserWithId)
async def read_users_me(user: UserWithId = Depends(get_current_user)):
    return user


@auth.post("/sign-up", response_model=UserWithId)
async def sing_up_new_user(user: UserWithPassword,
                           authentication_service: AuthenticationService = Depends(get_authentication_service)):
    try:
        user_id = await authentication_service.sign_up_user(user)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this login already exist"
        )

    return UserWithId(id=user_id, login=user.login)
