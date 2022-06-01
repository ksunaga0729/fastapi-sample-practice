from typing import List, Optional

from fastapi_sample import models
from fastapi_sample.schemas import user as user_schema
from fastapi_sample.utils.password import get_password_hash

from .base import BaseRepository


class UserRepository(BaseRepository):
    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return (
            self.session.query(models.User).filter(models.User.email == email).first()
        )

    def create_user(self, user_create: user_schema.UserCreate) -> models.User:
        hashed_password = get_password_hash(user_create.password)
        user = models.User(
            **user_create.dict(exclude={"password"}), password=hashed_password
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[models.User]:
        return (
            self.session.query(models.User)
            .order_by(models.User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_by_user_id(self, user_id: int) -> Optional[models.User]:
        return self.session.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[models.User]:
        return (
            self.session.query(models.User)
            .filter(models.User.username == username)
            .first()
        )

    def get_users_by_room_id(self, room_id) -> List[models.User]:
        return (
            self.session.query(models.User)
            .join(models.Member)
            .filter(models.Member.room_id == room_id)
            .all()
        )
