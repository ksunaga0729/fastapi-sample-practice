from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, RoomRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import message as message_schema
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class CreateMessageService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        message_repository: MessageRepository = Depends(
            get_repository(MessageRepository)
        ),
    ):
        self.__room_repository = room_repository
        self.__message_repository = message_repository

    def create_message(
        self, new_message: message_schema.MessageCreate, current_user: models.User
    ) -> models.Message:
        if not self.__room_repository.get_room_by_room_id(new_message.room_id):
            raise NotFoundException(message="room_id not found")

        if not self.__room_repository.get_member_by_room_and_user_id(
            room_id=new_message.room_id, user_id=current_user.id
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        message = self.__message_repository.create_message(new_message, current_user)
        return message
