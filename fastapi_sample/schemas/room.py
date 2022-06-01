from typing import Optional

from pydantic import BaseModel, Field

from .core import DateTimeModelMixin
from .message import MessagePublic


class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class RoomCreate(RoomBase):
    pass


class Room(DateTimeModelMixin, RoomBase):
    id: int

    class Config:
        orm_mode = True


class RoomPublic(DateTimeModelMixin, RoomBase):
    id: int
    last_message: Optional[MessagePublic]

    class Config:
        orm_mode = True


# 循環インポート回避のためのクラス
class MessageInRoom(MessagePublic):
    room: Room
