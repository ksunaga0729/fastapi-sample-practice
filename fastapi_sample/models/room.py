from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, Query, relationship

from .base import Base

if TYPE_CHECKING:
    from .member import Member as MemberModel
    from .message import Message as MessageModel


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, nullable=False)
    name: Mapped[str] = Column(String(255), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )

    messages: "Query[MessageModel]" = relationship(
        "Message",
        back_populates="room",
        order_by="desc(Message.created_at)",
        lazy="dynamic",
    )

    members: "MemberModel" = relationship("Member", back_populates="room")

    @property
    def last_message(self) -> "Optional[MessageModel]":
        return self.messages.first()
