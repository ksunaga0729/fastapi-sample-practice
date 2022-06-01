from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi_sample import models
from fastapi_sample.schemas import member as member_schema
from fastapi_sample.schemas import room as room_schema

from .base import BaseRepository


class RoomRepository(BaseRepository):
    def create_room_and_member(
        self,
        room_create: room_schema.RoomCreate,
        user: models.User,
    ) -> models.Room:
        room = models.Room(**room_create.dict())
        self.session.add(room)

        member = models.Member(
            user=user,
            room=room,
            member_role=member_schema.RoleList.host,
        )
        self.session.add(member)

        self.session.commit()

        self.session.refresh(room)
        self.session.refresh(member)

        return room

    def get_rooms(self) -> List[models.Room]:
        return self.session.query(models.Room).all()

    def get_room_by_room_id(self, room_id: int) -> Optional[models.Room]:
        return self.session.query(models.Room).filter(models.Room.id == room_id).first()

    def role_check(
        self,
        room_id: int,
        user: models.User,
    ) -> Optional[models.Member]:
        return (
            self.session.query(models.Member)
            .filter(
                models.Member.user_id == user.id,
                models.Member.room_id == room_id,
                models.Member.member_role == member_schema.RoleList.host,
            )
            .first()
        )

    def create_member(
        self,
        room_id: int,
        user_id: int,
    ) -> models.Member:
        member = models.Member(
            user_id=user_id,
            room_id=room_id,
            member_role=member_schema.RoleList.general,
        )
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)

        return member

    def get_room_by_user_id(self, user_id: int) -> List[models.Room]:
        return (
            self.session.query(models.Room)
            .join(models.Member)
            .filter(models.Member.user_id == user_id)
            .all()
        )

    def update_read_time(self, member: models.Member) -> None:
        jst = timezone(timedelta(hours=+9), "JST")

        member.read_at = datetime.now(jst)
        self.session.commit()
        self.session.refresh(member)

    def get_member_by_room_and_user_id(
        self,
        room_id: int,
        user_id: int,
    ) -> Optional[models.Member]:
        return (
            self.session.query(models.Member)
            .filter(
                models.Member.room_id == room_id,
                models.Member.user_id == user_id,
            )
            .first()
        )
