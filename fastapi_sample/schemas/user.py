from pydantic import BaseModel, EmailStr, Field

from .core import DateTimeModelMixin


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=7, max_length=100)


class User(DateTimeModelMixin, UserBase):
    id: int

    class Config:
        orm_mode = True


class UserPublic(DateTimeModelMixin):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserName(BaseModel):
    username: str
