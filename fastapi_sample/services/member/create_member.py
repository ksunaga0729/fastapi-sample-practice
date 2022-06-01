from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository, UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
)


class CreateMemberService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        user_repository: UserRepository = Depends(get_repository(UserRepository)),
    ):
        self.__room_repository = room_repository
        self.__user_repository = user_repository

    def create_member(
        self,
        room_id: int,
        user_name: str,
        current_user: models.User,
    ) -> models.Member:

        if self.__room_repository.get_room_by_room_id(room_id) is None:
            raise NotFoundException("room_id not found")

        user = self.__user_repository.get_user_by_username(user_name)
        if user is None:
            raise NotFoundException("user not found")
        if self.__room_repository.role_check(room_id, current_user) is None:
            raise ForbiddenException("Permission denied")
        if (
            self.__room_repository.get_member_by_room_and_user_id(room_id, user.id)
            is not None
        ):
            raise ConflictException("user already joined to room")

        member = self.__room_repository.create_member(room_id, user.id)

        return member
