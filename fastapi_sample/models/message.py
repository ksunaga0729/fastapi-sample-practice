from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .room import Room as RoomModel
    from .thread import Thread as ThreatModel
    from .user import User as UserModel


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    content: Mapped[str] = Column(String(255), unique=False, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )

    user: "UserModel" = relationship("User", back_populates="messages")
    room: "RoomModel" = relationship("Room", back_populates="messages")
    threads: "ThreatModel" = relationship("Thread", back_populates="message")
