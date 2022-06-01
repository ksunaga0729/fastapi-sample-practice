from typing import List

from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, RoomRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class GetMessagesByRoomIdService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        message_repository: MessageRepository = Depends(
            get_repository(MessageRepository)
        ),
    ):
        self.__room_repository = room_repository
        self.__message_repository = message_repository

    def get_messages_by_room_id(
        self, room_id: int, current_user_id: int
    ) -> List[models.Message]:
        if not self.__room_repository.get_room_by_room_id(room_id):
            raise NotFoundException(message="room_id not found")

        if not self.__room_repository.get_member_by_room_and_user_id(
            room_id=room_id, user_id=current_user_id
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        messages_list = self.__message_repository.get_messages_by_room_id(room_id)
        return messages_list
