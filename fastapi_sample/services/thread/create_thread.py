from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, RoomRepository, ThreadRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import thread as thread_schema
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class CreateThreadService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        message_repository: MessageRepository = Depends(
            get_repository(MessageRepository)
        ),
        thread_repository: ThreadRepository = Depends(get_repository(ThreadRepository)),
    ):
        self.__room_repository = room_repository
        self.__message_repository = message_repository
        self.__thread_repository = thread_repository

    def create_thread(
        self,
        message_id: int,
        thread: thread_schema.ThreadPublic,
        current_user: models.User,
    ) -> models.Thread:
        message = self.__message_repository.get_message_by_message_id(message_id)

        if message is None:
            raise NotFoundException(message="message_id not found")
        if not self.__room_repository.get_member_by_room_and_user_id(
            message.room_id, current_user.id
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        return self.__thread_repository.create_thread(
            message_id, thread.content, current_user
        )
