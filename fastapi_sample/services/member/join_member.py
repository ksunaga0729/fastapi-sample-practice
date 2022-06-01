from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ConflictException, NotFoundException


class JoinMemberService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
    ):
        self.__room_repository = room_repository

    def join_member(
        self,
        room_id: int,
        current_user: models.User,
    ) -> models.Member:

        if self.__room_repository.get_room_by_room_id(room_id) is None:
            raise NotFoundException("room_id not found")

        if (
            self.__room_repository.get_member_by_room_and_user_id(
                room_id, current_user.id
            )
            is not None
        ):
            raise ConflictException("user already joined to room")

        return self.__room_repository.create_member(room_id, current_user.id)
