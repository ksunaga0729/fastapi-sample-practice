from fastapi import Depends

from fastapi_sample.cruds import RoomRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class UpdateReadTimeService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
    ):
        self.__room_repository = room_repository

    def update_read_time(self, room_id: int, current_user_id: int):
        if self.__room_repository.get_room_by_room_id(room_id) is None:
            raise NotFoundException(message="room_id not found")

        member = self.__room_repository.get_member_by_room_and_user_id(
            room_id=room_id, user_id=current_user_id
        )
        if not member:
            raise ForbiddenException(message="You don't belong to the specified room")

        self.__room_repository.update_read_time(member)
