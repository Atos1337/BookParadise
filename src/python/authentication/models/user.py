from pydantic import BaseModel


class User(BaseModel):
    login: str


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str


class UserOut(UserIn):
    id: int
