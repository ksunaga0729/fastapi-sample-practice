from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import desc

from fastapi_sample import models
from fastapi_sample.schemas import message as message_schema

from .base import BaseRepository


class MessageRepository(BaseRepository):
    def get_messages(self) -> List[models.Message]:
        return (
            self.session.query(models.Message)
            .order_by(desc(models.Message.created_at))
            .all()
        )

    def get_message_by_message_id(self, message_id: int) -> Optional[models.Message]:
        return (
            self.session.query(models.Message)
            .filter(models.Message.id == message_id)
            .first()
        )

    def get_messages_by_userid(self, userid: int) -> List[models.Message]:
        return (
            self.session.query(models.Message)
            .filter(models.Message.user_id == userid)
            .order_by(desc(models.Message.created_at))
            .all()
        )

    def get_messages_by_room_id(self, room_id: int) -> List[models.Message]:
        return (
            self.session.query(models.Message)
            .filter(models.Message.room_id == room_id)
            .order_by(desc(models.Message.created_at))
            .all()
        )

    def get_message_by_message_and_room_id(
        self, message_id: int, room_id: int
    ) -> Optional[models.Message]:
        return (
            self.session.query(models.Message)
            .filter(models.Message.id == message_id, models.Message.room_id == room_id)
            .first()
        )

    def get_messages_by_content_and_room_id(
        self, content: str, room_id: int
    ) -> List[models.Message]:
        return (
            self.session.query(models.Message)
            .filter(
                models.Message.content.contains(content),
                models.Message.room_id == room_id,
            )
            .all()
        )

    def create_message(
        self,
        message_create: message_schema.MessageCreate,
        user: models.User,
    ) -> models.Message:
        message = models.Message(**message_create.dict(), user=user)
        self.session.add(message)
        self.session.commit()

        return message

    def delete_message(self, message: models.Message) -> None:
        self.session.delete(message)
        self.session.commit()

    def update_message_by_message_id(self, message: models.Message) -> models.Message:
        self.session.commit()
        self.session.refresh(message)

        return message

    def update_read_time(self, message_id: int) -> None:
        jst = timezone(timedelta(hours=+9), "JST")
        message = (
            self.session.query(models.Message)
            .filter(models.Message.id == message_id)
            .first()
        )

        if message:
            message.updated_at = datetime.now(jst)
            self.session.commit()
            self.session.refresh(message)
