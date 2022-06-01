from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .member import Member as MemberModel
    from .thread import Thread as ThreatModel
    from .message import Message as MessageModel

from fastapi_sample.utils.password import pwd_context


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, nullable=False)
    username: Mapped[str] = Column(String(255), unique=True, index=True, nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    password: Mapped[str] = Column(Text, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    is_superuser: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )

    messages: "MessageModel" = relationship("Message", back_populates="user")
    members: "MemberModel" = relationship("Member", back_populates="user")
    threads: "ThreatModel" = relationship("Thread", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
