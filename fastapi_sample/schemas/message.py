from pydantic import BaseModel, Field

from .core import DateTimeModelMixin
from .user import UserPublic


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=100)


class MessageCreate(MessageBase):
    room_id: int


class Message(DateTimeModelMixin, MessageBase):
    id: int
    user_id: int
    room_id: int

    class Config:
        orm_mode = True


class MessagePublic(DateTimeModelMixin, MessageBase):
    id: int
    room_id: int
    user: UserPublic

    class Config:
        orm_mode = True


class MessageUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=100)
