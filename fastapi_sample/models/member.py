from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .room import Room as RoomModel
    from .user import User as UserModel


class Member(Base):
    __tablename__ = "room_members"

    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )
    room_id: Mapped[int] = Column(
        Integer, ForeignKey("rooms.id"), primary_key=True, nullable=False
    )
    member_role: Mapped[str] = Column(String(255), nullable=False)

    read_at: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False)

    user: "UserModel" = relationship("User", back_populates="members")
    room: "RoomModel" = relationship("Room", back_populates="members")
