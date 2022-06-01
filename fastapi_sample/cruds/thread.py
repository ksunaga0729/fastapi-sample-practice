from typing import List, Optional

from sqlalchemy import desc

from fastapi_sample import models

from .base import BaseRepository


class ThreadRepository(BaseRepository):
    def get_thread_by_thread_id(self, thread_id: int) -> Optional[models.Thread]:
        return (
            self.session.query(models.Thread)
            .filter(models.Thread.id == thread_id)
            .first()
        )

    def create_thread(
        self, message_id: int, content: str, user: models.User
    ) -> models.Thread:
        thread = models.Thread(message_id=message_id, content=content, user=user)
        self.session.add(thread)
        self.session.commit()
        self.session.refresh(thread)

        return thread

    def update_thread_by_thread_and_user_id(
        self, thread: models.Thread, content: str
    ) -> models.Thread:
        thread.content = content
        self.session.commit()
        self.session.refresh(thread)

        return thread

    def get_threads(self) -> List[models.Thread]:
        return (
            self.session.query(models.Thread)
            .order_by(desc(models.Thread.created_at))
            .all()
        )

    def get_threads_message_id(self, message_id) -> List[models.Thread]:
        return (
            self.session.query(models.Thread)
            .filter(models.Thread.message_id == message_id)
            .order_by(desc(models.Thread.created_at))
            .all()
        )

    def delete_thread(self, thread: models.Thread) -> None:
        self.session.delete(thread)
        self.session.commit()
