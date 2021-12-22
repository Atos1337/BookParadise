from pydantic import BaseModel


class User(BaseModel):
    login: str


class UserWithPassword(User):
    password: str


class UserWithId(User):
    id: int
