from typing import Optional

from pydantic import BaseModel, Field

from .core import DateTimeModelMixin
from .message import MessagePublic


class ThreadBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=100)


class Thread(DateTimeModelMixin, ThreadBase):
    id: int
    user_id: int
    message: Optional[MessagePublic]

    class Config:
        orm_mode = True


class ThreadPublic(ThreadBase):
    pass
