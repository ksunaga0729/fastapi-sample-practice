from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message as MessageModel
    from .user import User as UserModel


class Thread(Base):
    __tablename__ = "message_threads"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, nullable=False)
    message_id: Mapped[int] = Column(Integer, ForeignKey("messages.id"), nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = Column(String(255), unique=False, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )

    user: "UserModel" = relationship("User", back_populates="threads")
    message: "MessageModel" = relationship("Message", back_populates="threads")
