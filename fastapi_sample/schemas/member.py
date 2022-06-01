from enum import Enum

from pydantic import BaseModel

from .core import ReadTimeModel
from .room import Room
from .user import UserPublic


class RoleList(str, Enum):
    host = "host"
    general = "general"


class MemberBase(BaseModel):
    user_id: int
    room_id: int
    member_role: RoleList = RoleList.general


class Member(MemberBase, ReadTimeModel):
    class Config:
        orm_mode = True


class MemberCreate(BaseModel):
    room: Room
    user: UserPublic

    class Config:
        orm_mode = True
